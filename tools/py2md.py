#!/usr/bin/env python3
"""실습 코드(.py)를 MkDocs 학습 노트(.md)로 변환한다.

사용법:
    python py2md.py week03/groupby.py
    python py2md.py docs/**/*.py
"""
import ast
import datetime
import pathlib
import re
import sys

MARK_RE = re.compile(r"^\s*#(==|>|!|\?)\s?(.*)$")
# #@@@ 는 issue_extract.py 가 처리하므로 노트/코드 양쪽에서 제외한다.
ISSUE_RE = re.compile(r"^\s*#@@@\s+")


def read_meta(src):
    """모듈 docstring에서 title/tags 등을 뽑고, docstring이 끝나는 줄 번호를 돌려준다."""
    meta, skip = {}, 0
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return meta, skip
    doc = ast.get_docstring(tree)
    if doc is None:
        return meta, skip
    skip = tree.body[0].end_lineno
    for line in doc.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip().lower()] = val.strip()
    return meta, skip


def parse(src, skip=0):
    body, stuck, questions = [], [], []
    code, hl = [], []
    pending_hl = False

    def flush():
        nonlocal code, hl
        while code and not code[-1].strip():
            code.pop()
        if code:
            body.append(("code", list(code), list(hl)))
        code, hl = [], []

    for lineno, raw in enumerate(src.splitlines(), 1):
        if lineno <= skip:
            continue
        if ISSUE_RE.match(raw):
            continue
        m = MARK_RE.match(raw)
        if m and not (lineno == 1 and raw.startswith("#!/")):
            tag, text = m.group(1), m.group(2).strip()
            if tag == "==":
                flush()
                body.append(("head", text, None))
            elif tag == ">":
                flush()
                if body and body[-1][0] == "prose":
                    body[-1] = ("prose", body[-1][1] + " " + text, None)
                else:
                    body.append(("prose", text, None))
            elif tag == "!":
                stuck.append(text)
                pending_hl = True
            elif tag == "?":
                questions.append(text)
            continue
        if not raw.strip() and not code:
            continue
        code.append(raw)
        if pending_hl:
            hl.append(len(code))
            pending_hl = False
    flush()
    return body, stuck, questions


def render(path, meta, body, stuck, questions):
    title = meta.get("title", path.stem)
    out = ["---", f"title: {title}"]
    out.append(f"date: {meta.get('date', datetime.date.today().isoformat())}")
    if "tags" in meta:
        out.append(f"tags: {meta['tags']}")
    out.append("---")
    out.append("")
    out.append(f"# {title}")
    out.append("")
    out.append(f"> 원본 코드: [`{path.name}`]({path.name})")
    out.append("")

    for kind, a, b in body:
        if kind == "head":
            out.append(f"## {a}")
            out.append("")
        elif kind == "prose":
            out.append(a)
            out.append("")
        else:
            fence = "```python"
            if b:
                fence += ' hl_lines="%s"' % " ".join(str(n) for n in b)
            out.append(fence)
            out.extend(a)
            out.append("```")
            out.append("")

    if stuck:
        out.append("## 막혔던 부분")
        out.append("")
        for s in stuck:
            out.append("!!! warning")
            out.append(f"    {s}")
            out.append("")

    if questions:
        out.append("## 다시 볼 것")
        out.append("")
        for q in questions:
            out.append(f"- [ ] {q}")
        out.append("")

    return "\n".join(out)


def convert(path):
    src = path.read_text(encoding="utf-8")
    meta, skip = read_meta(src)
    body, stuck, questions = parse(src, skip)
    target = path.with_suffix(".md")
    target.write_text(render(path, meta, body, stuck, questions), encoding="utf-8")
    return target


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("사용법: python py2md.py <파일.py> [...]")
    for arg in sys.argv[1:]:
        p = pathlib.Path(arg)
        if p.suffix == ".py" and p.name != "py2md.py":
            print("생성:", convert(p))
