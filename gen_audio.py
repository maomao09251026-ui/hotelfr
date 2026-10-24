#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 edge-tts（微软免费语音）批量生成 MP3，页面检测到 audio/manifest.json 就自动优先用 MP3。

用法（在你自己的电脑或 VPS 上，能上网即可）：
  pip install edge-tts
  python3 build.py
  python3 gen_audio.py            # 法语 + 中文 + 英文，约 900 个小文件，几分钟
  python3 gen_audio.py --fr-only  # 只生成法语
然后把 audio/ 目录一起 push 到 GitHub。

换声音：edge-tts --list-voices | grep fr-FR
  fr-FR-DeniseNeural 女声（默认） / fr-FR-HenriNeural 男声 / fr-FR-VivienneMultilingualNeural
"""
import asyncio, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(HERE, "audio")
os.makedirs(AUDIO, exist_ok=True)

VOICES = {"fr": "fr-FR-DeniseNeural", "zh": "zh-CN-XiaoxiaoNeural", "en": "en-US-JennyNeural"}
FR_ONLY = "--fr-only" in sys.argv

try:
    import edge_tts
except ImportError:
    sys.exit("先执行: pip install edge-tts")

js = open(os.path.join(HERE, "data.js"), encoding="utf-8").read()
data = json.loads(js.split("=", 1)[1].strip().rstrip(";"))

jobs = []
for d in data:
    for s in d["sents"]:
        jobs.append((s["id"] + "_fr", s["tf"], "fr"))
        if not FR_ONLY:
            jobs.append((s["id"] + "_zh", s["c"].split("（")[0], "zh"))
            jobs.append((s["id"] + "_en", s["e"], "en"))
    for v in d["vocab"]:
        jobs.append((v["id"] + "_fr", v["tf"], "fr"))
        if not FR_ONLY:
            jobs.append((v["id"] + "_zh", v["c"].split("（")[0].split(" / ")[0], "zh"))

sem = asyncio.Semaphore(6)

async def one(name, text, lang):
    path = os.path.join(AUDIO, name + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return
    async with sem:
        for attempt in range(3):
            try:
                rate = "-15%" if lang == "fr" else "+0%"
                await edge_tts.Communicate(text, VOICES[lang], rate=rate).save(path)
                return
            except Exception as e:
                if attempt == 2:
                    print("失败:", name, e)
                await asyncio.sleep(1.5)

async def main():
    await asyncio.gather(*(one(*j) for j in jobs))
    have = sorted(f[:-4] for f in os.listdir(AUDIO) if f.endswith(".mp3") and os.path.getsize(os.path.join(AUDIO, f)) > 0)
    json.dump(have, open(os.path.join(AUDIO, "manifest.json"), "w"))
    print(f"完成：{len(have)} 个音频，manifest.json 已写入")

asyncio.run(main())
