#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 docs/docs/*.md 的 frontmatter 与真实文件体积生成 docs/data.json。

字数与时长都在这里实测，不由人工填写，避免站点上的指标与内容脱钩。
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs", "docs")
AUDIO = os.path.join(ROOT, "docs", "audio")
OUT = os.path.join(ROOT, "docs", "data.json")

# 中文按字面速度折算，英文按词速 200 wpm 折算成分钟。
CJK_PER_MIN = 400
LATIN_WORDS_PER_MIN = 200

# Layer III 码率表，按 bitrate index 1..14 取值（单位 kbps）。
BITRATES = {
    3: [32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
    2: [8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
    0: [8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
}
# 版本位：11=MPEG1，10=MPEG2，00=MPEG2.5
SAMPLE_RATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000],
                0: [11025, 12000, 8000]}


def fm_get(text, key):
    m = re.search(r"^%s:\s*(.+)$" % key, text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def count_words(body):
    """正文字数 = 中文字符 + 英文词元，去掉代码块与 markdown 标记。"""
    t = re.sub(r"```[\s\S]*?```", "", body)
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"[#>*`|_~-]", " ", t)
    cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
    latin = len(re.findall(r"[A-Za-z][A-Za-z0-9_.+/@-]*", t))
    return cjk, latin


def mp3_minutes(path):
    """逐帧走带算时长，不假设固定码率。"""
    with open(path, "rb") as fh:
        data = fh.read()
    i = 0
    while i < len(data) - 4 and data[i] != 0xFF:
        i += 1
    seconds = 0.0
    frames = 0
    while i < len(data) - 4:
        b1, b2, b3 = data[i], data[i + 1], data[i + 2]
        if b1 != 0xFF or (b2 & 0xE0) != 0xE0:
            i += 1
            continue
        version = (b2 >> 3) & 0x03        # 3=MPEG1, 2=MPEG2, 0=MPEG2.5
        if (b2 >> 1) & 0x03 != 1:         # 只处理 Layer III
            i += 1
            continue
        br_idx = (b3 >> 4) & 0x0F
        sr_idx = (b3 >> 2) & 0x03
        pad = (b3 >> 1) & 0x01
        if version not in BITRATES or br_idx in (0, 15) or sr_idx == 3:
            i += 1
            continue
        kbps = BITRATES[version][br_idx - 1]
        rate = SAMPLE_RATES[version][sr_idx]
        spf = 1152 if version == 3 else 576
        unit = 144 if version == 3 else 72
        frame_len = int(unit * kbps * 1000 / rate) + pad
        if frame_len <= 0:
            i += 1
            continue
        seconds += spf / rate
        frames += 1
        i += frame_len
    return round(seconds / 60, 1) if frames else 0.0


def main():
    entries = []
    for path in sorted(glob.glob(os.path.join(DOCS, "*.md"))):
        name = os.path.basename(path)
        num = int(name.split("-")[0])
        raw = open(path, encoding="utf-8").read()
        body = re.sub(r"\A---.*?\n---\n", "", raw, flags=re.S)
        cjk, latin = count_words(body)
        audio = os.path.join(AUDIO, "%02d.mp3" % num)
        audio_min = mp3_minutes(audio) if os.path.exists(audio) else 0.0
        read_min = max(1, round(cjk / CJK_PER_MIN + latin / LATIN_WORDS_PER_MIN))
        repo = fm_get(raw, "repo")
        entries.append({
            "num": num,
            "title": fm_get(raw, "title"),
            "repo": repo,
            "url": "https://github.com/" + repo if repo else "",
            "category": fm_get(raw, "category"),
            "file": name,
            "audio": "%02d.mp3" % num if os.path.exists(audio) else "",
            "words": cjk + latin,
            "cjk": cjk,
            "readMinutes": read_min,
            "audioMinutes": audio_min,
        })

    if os.path.exists(OUT):
        old = json.load(open(OUT, encoding="utf-8"))
        if old == entries:
            print("data.json 已是最新（%d 条）" % len(entries))
            return 0

    missing = [e["num"] for e in entries if not e["audio"]]
    if missing:
        print("WARN 缺音频：%s" % missing, flush=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    total_w = sum(e["words"] for e in entries)
    total_a = round(sum(e["audioMinutes"] for e in entries), 1)
    total_r = sum(e["readMinutes"] for e in entries)
    print("写入 %d 条 | 字数 %d | 音频 %s 分钟 | 阅读 %d 分钟"
          % (len(entries), total_w, total_a, total_r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
