# 酒店法语 · 7天速成（法 / 谐音 / 中 / 英）

酒店保洁 + 洗衣房岗位口语，184 句 + 106 个高频词，7 天分场景，带复读/回想/随机播放。

## 文件
- `index.html` 页面（播放器）
- `data.js` 页面读的数据（由 content.py 生成，不要手改）
- `content.py` **内容源**：改句子 / 加句子只改这个
- `build.py` 把 content.py 编译成 data.js
- `gen_audio.py` 用 edge-tts 批量生成 MP3（可选，但强烈建议）
- `audio/` MP3 放这里；页面检测到 `audio/manifest.json` 就自动优先用 MP3，否则用手机自带法语语音

## 部署到 GitHub Pages
1. GitHub 新建仓库 `hotelfr`（Public）
2. 把本目录所有文件 push 上去（或网页端 Upload files）
3. 仓库 Settings → Pages → Branch 选 `main` / root → Save
4. 地址：`https://maomao09251026-ui.github.io/hotelfr/`

## 生成法语 MP3（在自己电脑上跑，几分钟）
```
pip install edge-tts
python3 build.py
python3 gen_audio.py        # 法+中+英；只要法语加 --fr-only
git add audio && git commit -m "audio" && git push
```

## 改内容
```
# 编辑 content.py，然后
python3 build.py
python3 gen_audio.py        # 只会补生成新增句子的音频，已有的跳过
```
iOS Safari 缓存：改完后把 index.html 里 `data.js?v=1` 和 `manifest.json?v=1` 的数字 +1。
