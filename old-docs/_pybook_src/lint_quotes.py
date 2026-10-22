#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描内容模块：找出会误终止 Python 三元引号字符串的写法。

合法用法只有两种：
  1) 行以 \"\"\"<section 开头（字符串起始）
  2) 行以 </section>\"\"\" 结尾（字符串结束，可带逗号/换行）
其余出现 \"\"\" 的地方（如示例代码里的文档字符串）都会破坏外层字符串。
"""
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '"""'


def main():
    for path in sorted(glob.glob(os.path.join(HERE, "content_*.py"))):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        for i, line in enumerate(lines, 1):
            if MARK not in line:
                continue
            s = line.strip()
            ok_start = s.startswith(MARK + "<section")
            ok_end = s.rstrip(",;").endswith("</section>" + MARK)
            if not (ok_start or ok_end):
                print("%s:%d: %s" % (os.path.basename(path), i, s))


if __name__ == "__main__":
    main()
