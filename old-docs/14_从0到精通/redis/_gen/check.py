# -*- coding: utf-8 -*-
import io, os, sys

ROOT = r"F:\跑路资料整理\技术栈详解DouBao\14_从0到精通\redis"
f = os.path.join(ROOT, "10_第一篇_入门与数据结构", "001_第1章_Redis是什么.html")
t = io.open(f, encoding="utf-8").read()
i = t.find("</main>")
out = []
out.append("index of </main> = %s" % i)
out.append(repr(t[i-300:i+900]))
i2 = t.find("doc-nav top")
out.append("--- top nav ---")
out.append(repr(t[i2-60:i2+400]))
io.open(os.path.join(ROOT, "_gen", "check.txt"), "w", encoding="utf-8").write("\n".join(out))
print("ok")
