#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java 从 0 到精通 · 章节文件与导航链接一次性校验
────────────────────────────────────────────────
校验内容：
  1) 全部 112 个章节文件名与编号精确一致（001-112 无缺失、无多余）
  2) 33 个新章节（080-112）的上一章/下一章 href 与约定清单逐字一致
  3) 新章节导航目标文件在磁盘上真实存在（112 的下一章 hidden 占位除外）
  4) 新章节文件为合法 UTF-8、可被 HTMLParser 解析
用法：python _verify_java_links.py
"""
import os
import re
import sys
from html.parser import HTMLParser

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "old-docs", "14_从0到精通", "java")

# 篇目录 -> 章节文件名（3 位编号 _ 第N章_ 标题）
PARTS = {
    "10_第一篇_入门与语法": 10, "20_第二篇_面向对象": 10, "30_第三篇_核心API与集合": 10,
    "40_第四篇_异常与IO": 8, "50_第五篇_反射注解与函数式": 8, "60_第六篇_并发编程": 12,
    "70_第七篇_JVM": 10, "80_第八篇_数据库与JDBC": 8, "90_第九篇_Spring核心": 10,
    "100_第十篇_SpringBoot与Web": 10, "110_第十一篇_工程化与测试": 8,
    "120_第十二篇_综合项目收官": 8,
}

# 新章节导航约定：rel_path -> (prev_href, next_href 或 None=hidden占位)
NAV = {
    "90_第九篇_Spring核心/080_第80章_Bean作用域与懒加载.html": ("079_第79章_依赖注入三种方式与选择.html", "081_第81章_AOP概念与动态代理回顾.html"),
    "90_第九篇_Spring核心/081_第81章_AOP概念与动态代理回顾.html": ("080_第80章_Bean作用域与懒加载.html", "082_第82章_切面实战日志与耗时统计.html"),
    "90_第九篇_Spring核心/082_第82章_切面实战日志与耗时统计.html": ("081_第81章_AOP概念与动态代理回顾.html", "083_第83章_声明式事务与传播行为.html"),
    "90_第九篇_Spring核心/083_第83章_声明式事务与传播行为.html": ("082_第82章_切面实战日志与耗时统计.html", "084_第84章_事件机制与监听器.html"),
    "90_第九篇_Spring核心/084_第84章_事件机制与监听器.html": ("083_第83章_声明式事务与传播行为.html", "085_第85章_循环依赖与三级缓存.html"),
    "90_第九篇_Spring核心/085_第85章_循环依赖与三级缓存.html": ("084_第84章_事件机制与监听器.html", "086_第86章_自动装配原理前奏.html"),
    "90_第九篇_Spring核心/086_第86章_自动装配原理前奏.html": ("085_第85章_循环依赖与三级缓存.html", "../100_第十篇_SpringBoot与Web/087_第87章_SpringBoot入门与启动流程.html"),
    "100_第十篇_SpringBoot与Web/087_第87章_SpringBoot入门与启动流程.html": ("../90_第九篇_Spring核心/086_第86章_自动装配原理前奏.html", "088_第88章_配置体系与多环境.html"),
    "100_第十篇_SpringBoot与Web/088_第88章_配置体系与多环境.html": ("087_第87章_SpringBoot入门与启动流程.html", "089_第89章_Web开发与RESTful接口.html"),
    "100_第十篇_SpringBoot与Web/089_第89章_Web开发与RESTful接口.html": ("088_第88章_配置体系与多环境.html", "090_第90章_参数校验Validation.html"),
    "100_第十篇_SpringBoot与Web/090_第90章_参数校验Validation.html": ("089_第89章_Web开发与RESTful接口.html", "091_第91章_全局异常处理与统一响应.html"),
    "100_第十篇_SpringBoot与Web/091_第91章_全局异常处理与统一响应.html": ("090_第90章_参数校验Validation.html", "092_第92章_MyBatis整合与Mapper.html"),
    "100_第十篇_SpringBoot与Web/092_第92章_MyBatis整合与Mapper.html": ("091_第91章_全局异常处理与统一响应.html", "093_第93章_分页与通用查询.html"),
    "100_第十篇_SpringBoot与Web/093_第93章_分页与通用查询.html": ("092_第92章_MyBatis整合与Mapper.html", "094_第94章_JWT登录实战.html"),
    "100_第十篇_SpringBoot与Web/094_第94章_JWT登录实战.html": ("093_第93章_分页与通用查询.html", "095_第95章_文件上传与静态资源.html"),
    "100_第十篇_SpringBoot与Web/095_第95章_文件上传与静态资源.html": ("094_第94章_JWT登录实战.html", "096_第96章_定时任务与异步处理.html"),
    "100_第十篇_SpringBoot与Web/096_第96章_定时任务与异步处理.html": ("095_第95章_文件上传与静态资源.html", "../110_第十一篇_工程化与测试/097_第97章_Maven依赖与生命周期.html"),
    "110_第十一篇_工程化与测试/097_第97章_Maven依赖与生命周期.html": ("../100_第十篇_SpringBoot与Web/096_第96章_定时任务与异步处理.html", "098_第98章_多模块项目组织.html"),
    "110_第十一篇_工程化与测试/098_第98章_多模块项目组织.html": ("097_第97章_Maven依赖与生命周期.html", "099_第99章_单元测试JUnit5与Mockito.html"),
    "110_第十一篇_工程化与测试/099_第99章_单元测试JUnit5与Mockito.html": ("098_第98章_多模块项目组织.html", "100_第100章_日志体系Logback与链路.html"),
    "110_第十一篇_工程化与测试/100_第100章_日志体系Logback与链路.html": ("099_第99章_单元测试JUnit5与Mockito.html", "101_第101章_代码规范Checkstyle与评审.html"),
    "110_第十一篇_工程化与测试/101_第101章_代码规范Checkstyle与评审.html": ("100_第100章_日志体系Logback与链路.html", "102_第102章_打包与部署jar镜像.html"),
    "110_第十一篇_工程化与测试/102_第102章_打包与部署jar镜像.html": ("101_第101章_代码规范Checkstyle与评审.html", "103_第103章_Docker化SpringBoot应用.html"),
    "110_第十一篇_工程化与测试/103_第103章_Docker化SpringBoot应用.html": ("102_第102章_打包与部署jar镜像.html", "104_第104章_性能优化入门接口耗时分析.html"),
    "110_第十一篇_工程化与测试/104_第104章_性能优化入门接口耗时分析.html": ("103_第103章_Docker化SpringBoot应用.html", "../120_第十二篇_综合项目收官/105_第105章_综合项目需求管理系统设计.html"),
    "120_第十二篇_综合项目收官/105_第105章_综合项目需求管理系统设计.html": ("../110_第十一篇_工程化与测试/104_第104章_性能优化入门接口耗时分析.html", "106_第106章_后端实现接口与分层.html"),
    "120_第十二篇_综合项目收官/106_第106章_后端实现接口与分层.html": ("105_第105章_综合项目需求管理系统设计.html", "107_第107章_前后端联调与跨域.html"),
    "120_第十二篇_综合项目收官/107_第107章_前后端联调与跨域.html": ("106_第106章_后端实现接口与分层.html", "108_第108章_缓存接入Redis模板.html"),
    "120_第十二篇_综合项目收官/108_第108章_缓存接入Redis模板.html": ("107_第107章_前后端联调与跨域.html", "109_第109章_消息队列接入与异步解耦.html"),
    "120_第十二篇_综合项目收官/109_第109章_消息队列接入与异步解耦.html": ("108_第108章_缓存接入Redis模板.html", "110_第110章_压测与调优闭环.html"),
    "120_第十二篇_综合项目收官/110_第110章_压测与调优闭环.html": ("109_第109章_消息队列接入与异步解耦.html", "111_第111章_面试知识体系梳理.html"),
    "120_第十二篇_综合项目收官/111_第111章_面试知识体系梳理.html": ("110_第110章_压测与调优闭环.html", "112_第112章_进阶路线微服务与云原生.html"),
    "120_第十二篇_综合项目收官/112_第112章_进阶路线微服务与云原生.html": ("111_第111章_面试知识体系梳理.html", None),
}


class NavParser(HTMLParser):
    """抓取 doc-nav 内的 a[href]，按出现顺序保存"""
    def __init__(self):
        super().__init__()
        self.in_nav = 0
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "nav" and "doc-nav" in d.get("class", ""):
            self.in_nav += 1
        if self.in_nav and tag == "a" and "href" in d:
            self.links.append((d.get("href", ""), d.get("class", "")))

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_nav:
            self.in_nav -= 1


def main():
    errors = []

    # 1) 全量章节文件盘点
    chapters = {}
    for part, count in PARTS.items():
        p = os.path.join(BASE, part)
        if not os.path.isdir(p):
            errors.append(f"篇目录缺失: {part}")
            continue
        for fn in sorted(os.listdir(p)):
            m = re.match(r"^(\d{3})_第(\d+)章_", fn)
            if fn.endswith(".html") and m:
                chapters[int(m.group(2))] = os.path.join(p, fn)
    got = sorted(chapters)
    missing = [n for n in range(1, 113) if n not in chapters]
    extra = [n for n in got if n < 1 or n > 112]
    if missing:
        errors.append(f"缺失章节: {missing}")
    if extra:
        errors.append(f"编号越界: {extra}")
    print(f"[1] 章节文件总数: {len(chapters)}（应为 112） 缺失: {missing or '无'} 越界: {extra or '无'}")

    # 2) 新章节导航逐字核对 + 目标存在性
    for rel, (prev_exp, next_exp) in NAV.items():
        full = os.path.join(BASE, rel)
        if not os.path.isfile(full):
            errors.append(f"新章节文件不存在: {rel}")
            continue
        try:
            with open(full, "r", encoding="utf-8") as f:
                html = f.read()
        except UnicodeDecodeError:
            errors.append(f"非 UTF-8: {rel}")
            continue
        parser = NavParser()
        parser.feed(html)
        links = [h for h, c in parser.links]
        if len(links) != 6:
            errors.append(f"{rel}: doc-nav 链接数 {len(links)} != 6（top+bottom 共 3×2）")
            continue
        top, bottom = links[:3], links[3:]
        if top != bottom:
            errors.append(f"{rel}: top/bottom 导航不一致 top={top} bottom={bottom}")
        # 0=上一章 1=返回首页 2=下一章
        if top[0] != prev_exp:
            errors.append(f"{rel}: 上一章 href={top[0]!r} 期望={prev_exp!r}")
        if top[1] != "../../../index.html":
            errors.append(f"{rel}: 返回首页 href={top[1]!r} 期望=../../../index.html")
        if next_exp is not None:
            if top[2] != next_exp:
                errors.append(f"{rel}: 下一章 href={top[2]!r} 期望={next_exp!r}")
            tgt = os.path.normpath(os.path.join(os.path.dirname(full), next_exp))
            if not os.path.isfile(tgt):
                errors.append(f"{rel}: 下一章目标不存在 -> {next_exp}")
        else:
            # 112：下一章为 hidden 占位
            if "hidden" not in top[2] and "hidden" not in " ".join(c for h, c in parser.links[:3]):
                errors.append(f"{rel}: 末章下一章应为 hidden 占位，实际 {top[2]!r}")
        # 上一章目标存在性
        tgtp = os.path.normpath(os.path.join(os.path.dirname(full), prev_exp))
        if not os.path.isfile(tgtp):
            errors.append(f"{rel}: 上一章目标不存在 -> {prev_exp}")
    print(f"[2] 新章节导航核对: {len(NAV)} 个文件全部处理")

    # 3) 新章节 HTML 可解析性
    bad = []
    for rel in NAV:
        full = os.path.join(BASE, rel)
        try:
            with open(full, "r", encoding="utf-8") as f:
                html = f.read()
            parser = NavParser()
            parser.feed(html)  # 解析异常会抛出
        except Exception as e:
            bad.append(f"{rel}: {e}")
    print(f"[3] HTML 解析: {len(NAV) - len(bad)}/{len(NAV)} 通过" + (f"  异常: {bad}" if bad else ""))

    if errors:
        print("\n==== 校验失败 ====")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("\n==== 校验全部通过：112 章齐备，新 33 章导航与文件名精确一致 ====")


if __name__ == "__main__":
    main()
