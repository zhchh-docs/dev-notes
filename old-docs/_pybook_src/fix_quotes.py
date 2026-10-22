#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量修正内容模块里会误终止三元引号字符串的写法。

规则：
  1. 跳过文件第 2 行的模块说明（合法用法）；
  2. 若该行是 HTML 正文里讲解「三元引号」写法的说明行 → 转义为 &quot; 实体；
  3. 其余（即示例代码里的 Python 文档字符串）→ 换成 '''，保持示例仍是合法 Python。
"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '"""'


def fix_line(line):
    if "<code>" in line and MARK in line:
        return line.replace(MARK, "&quot;&quot;&quot;")
    return line.replace(MARK, "'''")


def main():
    changed = []
    for path in sorted(glob.glob(os.path.join(HERE, "content_p2*.py"))):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines(keepends=True)
        touched = False
        for i, line in enumerate(lines):
            if i == 1 or MARK not in line:          # 跳过模块说明行
                continue
            s = line.strip()
            if s.startswith(MARK + "<section") or s.rstrip(",;").endswith("</section>" + MARK):
                continue                            # 合法的分节定界
            lines[i] = fix_line(line)
            touched = True
        if touched:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write("".join(lines))
            changed.append(os.path.basename(path))
    print("已修正:", ", ".join(changed) or "无")


if __name__ == "__main__":
    main()
