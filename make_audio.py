# -*- coding: utf-8 -*-
"""把 docs/*.md 教程转成 audio/NN.mp3，供教程站播放。"""
import re, glob, os, sys, asyncio
import edge_tts

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
AUDIO = os.path.join(ROOT, "audio")
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+12%"


def md_to_text(md: str) -> str:
    # 去掉 frontmatter
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    # 代码块 -> 占位说明
    md = re.sub(r"```[\s\S]*?```", "（这里是一段代码示例，详见网页版。）", md)
    # 行内代码、图片、链接
    md = re.sub(r"`([^`]*)`", r"\1", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    # 标题转口播提示
    md = re.sub(r"^#{1,4}\s*(.+)$", r"\1。", md, flags=re.M)
    # 表格行去掉竖线
    md = re.sub(r"^\|.*$", lambda m: m.group(0).replace("|", "，").strip("，"), md, flags=re.M)
    # 强调符号
    md = re.sub(r"[*_~>#]+", "", md)
    # 多余空行
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


async def gen(md_path: str):
    name = os.path.basename(md_path)
    num = name.split("-")[0]
    out = os.path.join(AUDIO, f"{num}.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return f"skip {name}"
    text = md_to_text(open(md_path, encoding="utf-8").read())
    tts = edge_tts.Communicate(text, VOICE, rate=RATE)
    await tts.save(out)
    return f"done {name} -> {os.path.getsize(out)//1024}KB"


async def main():
    os.makedirs(AUDIO, exist_ok=True)
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    files = sorted(glob.glob(os.path.join(DOCS, "*.md")))
    if only:
        files = [f for f in files if any(o in f for o in only)]
    for f in files:
        try:
            print(await gen(f), flush=True)
        except Exception as e:
            print(f"FAIL {os.path.basename(f)}: {e}", flush=True)
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
