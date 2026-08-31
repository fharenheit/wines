#!/usr/bin/env python3
"""모든 마크다운 문서에 목차를 생성해 삽입한다.

계층 판정
    이 저장소는 문서마다 h1(`#`)과 h2(`##`)를 절 구분에 섞어 쓴다.
    그래서 마크다운 레벨만으로는 계층을 알 수 없어 다음 규칙을 쓴다.

    상위 항목 : h1. 그리고 h1이 아직 없거나 직전 h1도 번호를 달고 있을 때의
                번호(`1.` `2.` …) 붙은 h2 — 같은 번호 계열의 형제 절이므로.
    하위 항목 : 그 밖의 h2 중 앞에 h1이 있는 것.

    그래서 `# 6. 품종` 아래의 `## 스타일 대비`는 들여쓰이고 `## 7. 알아둘 이름`은
    형제로 남는 반면, `# 북부 론` 아래의 `## 1. 코트로티`는 들여쓰인다.

삽입 위치
    제목과 도입부 뒤, 첫 절 제목 앞. 사이의 `---` 구분선은 목차 아래로 옮긴다.
    <!-- toc --> ... <!-- /toc --> 로 감싸므로 여러 번 실행해도 결과가 같다.

    python3 scripts/make_toc.py            # 전체 갱신
    python3 scripts/make_toc.py --check    # 갱신이 필요한 문서만 보고 (수정 안 함)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- toc -->", "<!-- /toc -->"
TITLE = "## 목차"
MIN_ENTRIES = 3


def clean(text):
    """표시용 문자열 — 강조·코드·링크 표기를 벗긴다."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def slug(text, seen):
    """GitHub(github-slugger)의 앵커 생성 규칙."""
    s = re.sub(r"<[^>]+>", "", text).lower().strip()
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    s = s.replace(" ", "-")
    n = seen.get(s, 0)
    seen[s] = n + 1
    return s if n == 0 else "%s-%d" % (s, n)


def headings(lines):
    """(줄번호, 레벨, 원문). 코드 펜스 안은 건너뛴다."""
    out, fence = [], False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
            continue
        if not fence:
            m = re.match(r"(#{1,6})\s+(.*)", line)
            if m:
                out.append((i, len(m.group(1)), m.group(2).rstrip()))
    return out


def build(lines):
    """(목차 블록, 삽입 시작 줄, 삽입 끝 줄). 대상이 없으면 (None, 0, 0)."""
    hs = headings(lines)
    if not hs:
        return None, 0, 0

    seen = {}
    slugs = [slug(clean(t), seen) for _, _, t in hs]   # 중복 번호는 문서 전체 기준
    body = [(i, lv, t, sl) for (i, lv, t), sl in zip(hs, slugs)][1:]
    entries = [e for e in body if e[1] <= 2 and clean(e[2]) != "목차"]
    if len(entries) < MIN_ENTRIES:
        return None, 0, 0

    out, h1_numbered = [], None      # None = 본문에 아직 h1이 없다
    for _, level, text, sl in entries:
        text = clean(text)
        numbered = bool(re.match(r"\d+\.", text))
        if level == 1:
            h1_numbered = numbered
            top = True
        elif numbered:
            top = h1_numbered is None or h1_numbered
        else:
            top = h1_numbered is None
        out.append("%s- [%s](#%s)" % ("" if top else "  ", text, sl))

    # 첫 절 제목 앞의 빈 줄과 `---` 구분선 하나를 흡수한다.
    end = entries[0][0]
    start, rule = end, False
    while start - 1 > hs[0][0]:
        stripped = lines[start - 1].strip()
        if stripped == "":
            start -= 1
        elif stripped == "---" and not rule:
            rule = True
            start -= 1
        else:
            break

    block = ["", BEGIN, TITLE, ""] + out + ["", END, ""]
    if rule:
        block += ["---", ""]
    return block, start, end


def strip_old(lines):
    if BEGIN not in lines or END not in lines:
        return lines
    b, e = lines.index(BEGIN), lines.index(END)
    tail = e + 1
    while tail < len(lines) and lines[tail].strip() == "":
        tail += 1
    head = b
    while head - 1 >= 0 and lines[head - 1].strip() == "":
        head -= 1
    return lines[:head] + [""] + lines[tail:]


def run(check=False):
    changed, skipped = [], []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith((".", "__"))]
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ROOT)
            original = open(path, encoding="utf-8").read()
            lines = strip_old(original.split("\n"))
            block, start, end = build(lines)
            if block is None:
                skipped.append(rel)
                continue
            new = "\n".join(lines[:start] + block + lines[end:])
            if new != original:
                changed.append(rel)
                if not check:
                    open(path, "w", encoding="utf-8").write(new)
    print("%s: %d개" % ("갱신 필요" if check else "갱신", len(changed)))
    for c in changed:
        print("  " + c)
    if skipped:
        print("건너뜀(절 %d개 미만): %s" % (MIN_ENTRIES, ", ".join(skipped)))
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(run(check="--check" in sys.argv))
