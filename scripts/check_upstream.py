#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核对 docs/data.json 里的上游仓库是否仍然成立。

检查三件事：仓库是否改名/迁移、是否被归档或停更、正文里写的 star 数是否还在
±25% 误差内。CI 每次跑，清单漂移就报警，而不是等人肉发现。
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "docs", "data.json")
STALE_DAYS = 365
DRIFT = 0.25


def api(repo, token):
    req = urllib.request.Request("https://api.github.com/repos/" + repo,
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "oss-50-check"})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:                       # 404 / 限流 / 网络
        return {"__error__": str(e)}


def claimed_stars(text):
    """从标题里抽 star 数：'12k star'、'12k+ star'、'1.2 万 star'。"""
    out = []
    for m in re.finditer(r"([0-9][0-9.]*)\s*(k|万)\+?\s*star", text, re.I):
        v = float(m.group(1)) * (1000 if m.group(2).lower() == "k" else 10000)
        out.append((m.group(0), int(v)))
    return out


def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    entries = json.load(open(DATA, encoding="utf-8"))
    errors, warns = [], []
    for e in entries:
        j = api(e["repo"], token)
        if "__error__" in j:
            errors.append("%2d %s :: 取不到（%s）" % (e["num"], e["repo"], j["__error__"]))
            continue
        name = j["full_name"]
        if name != e["repo"]:
            errors.append("%2d %s :: 已迁移，应为 %s" % (e["num"], e["repo"], name))
            continue
        if j.get("archived"):
            warns.append("%2d %s :: 已归档（archived）" % (e["num"], name))
        pushed = (j.get("pushed_at") or "")[:10]
        try:
            idle = (date.today() - date.fromisoformat(pushed)).days
        except ValueError:
            idle = 0
        if idle > STALE_DAYS:
            warns.append("%2d %s :: %d 天没提交（%s）" % (e["num"], name, idle, pushed))
        got = j.get("stargazers_count", 0)
        for label, want in claimed_stars(e["title"]):
            if got < want * (1 - DRIFT):
                warns.append("%2d %s :: 标称 %s star，实际只有 %d" % (e["num"], name, label, got))
            elif got > want * (1 + DRIFT):
                warns.append("%2d %s :: 标称 %s star，实际已到 %d" % (e["num"], name, label, got))
    for line in errors:
        print("ERROR  " + line)
    for line in warns:
        print("WARN   " + line)
    print("核对 %d 个仓库：%d 条必须修，%d 条待复核" % (len(entries), len(errors), len(warns)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
