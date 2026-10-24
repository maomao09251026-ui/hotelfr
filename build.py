#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 content.py 编译成 data.js（页面读的数据）。改完 content.py 跑一次：python3 build.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, "content.py"), encoding="utf-8").read(), ns)
DAYS = ns["DAYS"]

def tts_text(s):
    # "désolé(e)" 读作 désolé；去掉法式引号
    return re.sub(r"\(e\)", "", s).replace("«", "").replace("»", "").strip()

out = []
for d in DAYS:
    sents = []
    k = 0
    for scene, rows in d["scenes"]:
        for f, x, c, e in rows:
            k += 1
            sents.append({"id": f"s{d['d']}_{k:02d}", "sc": scene, "f": f, "x": x, "c": c, "e": e, "tf": tts_text(f)})
    vocab = []
    for i, (f, x, c, e) in enumerate(d["vocab"], 1):
        vocab.append({"id": f"v{d['d']}_{i:02d}", "f": f, "x": x, "c": c, "e": e, "tf": tts_text(f)})
    out.append({"d": d["d"], "title": d["title"], "goal": d["goal"], "sents": sents, "vocab": vocab})

js = "window.HOTELFR = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(os.path.join(HERE, "data.js"), "w", encoding="utf-8").write(js)
n = sum(len(d["sents"]) for d in out); v = sum(len(d["vocab"]) for d in out)
print(f"data.js 已生成：{n} 句 + {v} 词")
