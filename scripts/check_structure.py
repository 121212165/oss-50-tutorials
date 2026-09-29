#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 50 篇教程的骨架完整：frontmatter 字段齐全 + 7 个规定小节 + 音频文件存在。"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs", "docs")
AUDIO = os.path.join(ROOT, "docs", "audio")
REQUIRED = ["它是什么", "为什么", "架构拆解", "上手路径", "进阶玩法", "横向对比", "认知红利"]
FIELDS = ["num", "title", "repo", "category", "minutes"]


def main():
    bad = []
    files = sorted(glob.glob(os.path.join(DOCS, "*.md")))
    if len(files) != 50:
        bad.append("教程篇数 %d，应为 50" % len(files))
    for path in files:
        name = os.path.basename(path)
        num = name.split("-")[0]
        raw = open(path, encoding="utf-8").read()
        fm = re.match(r"\A---\n(.*?)\n---\n", raw, re.S)
        if not fm:
            bad.append("%s :: 缺 frontmatter" % name)
            continue
        for f in FIELDS:
            if not re.search(r"^%s:\s*\S" % f, fm.group(1), re.M):
                bad.append("%s :: frontmatter 缺字段 %s" % (name, f))
        body = raw[fm.end():]
        h2 = re.findall(r"^##\s+(.*)", body, re.M)
        for want in REQUIRED:
            if not any(want in h for h in h2):
                bad.append("%s :: 缺小节「%s」" % (name, want))
        if not os.path.exists(os.path.join(AUDIO, "%s.mp3" % num)):
            bad.append("%s :: 缺音频 %s.mp3" % (name, num))
    data_path = os.path.join(ROOT, "docs", "data.json")
    if os.path.exists(data_path):
        index = json.load(open(data_path, encoding="utf-8"))
        listed = {e["file"] for e in index}
        actual = {os.path.basename(p) for p in files}
        for miss in sorted(actual - listed):
            bad.append("data.json :: 缺条目 %s" % miss)
        for ghost in sorted(listed - actual):
            bad.append("data.json :: 指向不存在的 %s" % ghost)
    for b in bad:
        print("FAIL " + b)
    print("结构校验：%d 篇，%d 条问题" % (len(files), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
