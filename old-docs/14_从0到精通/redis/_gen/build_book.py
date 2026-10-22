# -*- coding: utf-8 -*-
"""《Redis 从 0 到精通》54 章装配脚本（临时工具，成书后删除）。
复用 00_目录.html 的内联 CSS 与脚本块，逐章拼装 _gen/frag/cNNN.html 内容片段。
"""
import os, sys, re

ROOT = r"F:\跑路资料整理\技术栈详解DouBao\14_从0到精通\redis"
FRAG = os.path.join(ROOT, "_gen", "frag")
SRC = os.path.join(ROOT, "00_目录.html")

src = open(SRC, encoding="utf-8").read()
STYLE = src[src.index("<style>") + 7: src.index("</style>")]
i = src.index('<button id="backTop"')
j = src.index("<script>", i)
k = src.index('<script src="../../glossary/glossary-data.js">', j)
SCRIPTS = src[j:k].rstrip() + "\n"

CHAP_CSS = """
/* ===== 教科书章页专属 ===== */
.ex-box{border-left:4px solid var(--ok);background:var(--ok-soft);border-radius:0 8px 8px 0;padding:12px 16px;margin:14px 0;font-size:14px;line-height:1.8}
.ex-box .ex-tag{font-weight:700;color:var(--ok);margin-right:8px;white-space:nowrap}
section.card h2 .num{font-size:14px;letter-spacing:-.02em}
"""

FAVICON = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
           "viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%232d6a3f'/%3E%3Crect x='3' y='4' "
           "width='10' height='2' rx='1' fill='%23fff'/%3E%3Crect x='3' y='7' width='7' height='2' rx='1' "
           "fill='%23fff'/%3E%3Crect x='3' y='10' width='9' height='2' rx='1' fill='%23fff'/%3E%3C/svg%3E\">")

PART_DIR = {
    1: "10_第一篇_入门与数据结构",
    2: "20_第二篇_持久化与内存",
    3: "30_第三篇_缓存策略",
    4: "40_第四篇_分布式锁与原子",
    5: "50_第五篇_高可用与集群",
}
PART_NAME = {
    1: "第一篇 入门与数据结构",
    2: "第二篇 持久化与内存",
    3: "第三篇 缓存策略",
    4: "第四篇 分布式锁与原子",
    5: "第五篇 高可用与集群",
}

# (num, part, title, filename, minutes, level, hero_desc)
CHAPTERS = [
    (1, 1, "Redis 是什么：内存 KV 的定位", "001_第1章_Redis是什么.html", 30, "零基础可读",
     "在敲第一个 SET 之前，先回答三个问题：Redis 是什么？它解决什么问题？它和 MySQL 是什么关系？这一章不装环境，只建立全景地图。"),
    (2, 1, "安装与 redis-cli 入门", "002_第2章_安装与redis-cli入门.html", 35, "零基础可读",
     "把 Redis 真正跑起来：Windows/Linux/Docker 三种安装姿势、redis-cli 的常用技巧、CONFIG 与 INFO 的第一次亲密接触。"),
    (3, 1, "通用命令与 key 设计规范", "003_第3章_通用命令与key设计规范.html", 35, "零基础可读",
     "KEYS 为什么是生产禁令？SCAN 怎么用才正确？一套让团队受益三年的 key 命名规范，本章一次讲透。"),
    (4, 1, "String：缓存、计数与锁雏形", "004_第4章_String缓存计数与锁雏形.html", 35, "零基础可读",
     "最简单的结构往往藏着最多的细节：SET 的完整参数、INCR 的原子性、SETNX 与分布式锁的雏形，都在这一章。"),
    (5, 1, "Hash：对象字段级操作", "005_第5章_Hash对象字段级操作.html", 30, "零基础可读",
     "把一个对象拆成字段存进 Redis：HSET/HGETALL 的正确姿势、field 级过期为什么做不到、Hash 与 String 存对象的取舍。"),
    (6, 1, "List：列表与简单队列", "006_第6章_List列表与简单队列.html", 30, "零基础可读",
     "双向链表还是压缩列表？LPUSH+BRPOP 的经典队列模型、 trimming 旧数据、List 在消息场景的能力边界。"),
    (7, 1, "Set：去重与集合运算", "007_第7章_Set去重与集合运算.html", 30, "零基础可读",
     "无序不重复的魔法：抽奖、共同关注、标签系统——SINTER/SUNION/SDIFF 三个集合运算撑起一半业务场景。"),
    (8, 1, "ZSet：排行榜的核心", "008_第8章_ZSet排行榜的核心.html", 35, "零基础可读",
     "Redis 最强大也最常被低估的结构：跳表如何让排行榜又快又有序，ZRANGE/ZINCRBY/BYSCORE 全家桶实战。"),
    (9, 1, "位图、HyperLogLog 与 GEO", "009_第9章_位图HyperLogLog与GEO.html", 35, "需第一篇前 8 章基础",
     "三种特殊结构解决三类特殊问题：签到用 Bitmap、亿级 UV 用 HyperLogLog、附近的人用 GEO——每个都只要几 MB 内存。"),
    (10, 1, "过期机制：TTL 的真相", "010_第10章_过期机制TTL的真相.html", 30, "零基础可读",
     "key 到期就一定被删吗？惰性删除与定期删除的分工、过期 key 的三种命运、为什么 SET 同名 key 会清掉 TTL。"),
    (11, 1, "数据结构选型实战五例", "011_第11章_数据结构选型实战五例.html", 35, "需第一篇基础",
     "把前十章串起来：五个真实业务（购物车、签到、Feed 流、点赞、搜索联想）各选什么结构、为什么、怎么避坑。"),

    (12, 2, "RDB 快照：原理与配置", "012_第12章_RDB快照原理与配置.html", 35, "需第一篇基础",
     "fork + COW 是 RDB 的灵魂：save 参数怎么配、bgsave 期间写请求会不会卡、RDB 文件损坏了怎么救。"),
    (13, 2, "AOF 追加日志：三种刷盘", "013_第13章_AOF追加日志三种刷盘.html", 35, "需第一篇基础",
     "appendfsync 的 always/everysec/no 三档取舍、AOF 重写如何瘦身日志、AOF 文件损坏的修复手段。"),
    (14, 2, "混合持久化与选型", "014_第14章_混合持久化与选型.html", 30, "需第二篇前两章基础",
     "aof-use-rdb-preamble 的 4.0 王炸：RDB 的快+AOF 的全。RDB/AOF/混合/全关四种方案的决策树。"),
    (15, 2, "内存淘汰策略详解", "015_第15章_内存淘汰策略详解.html", 35, "需第二篇基础",
     "八种 maxmemory-policy 逐个拆解：LRU 与 LFU 的区别、volatile 与 allkeys 的取舍、业务该怎么选。"),
    (16, 2, "maxmemory 与容量规划", "016_第16章_maxmemory与容量规划.html", 30, "需第二篇基础",
     "maxmemory 别配成机器内存的 100%：碎片、fork、复制缓冲区都要留活口。一套可落地的容量估算公式。"),
    (17, 2, "大 key：发现与治理", "017_第17章_大key发现与治理.html", 35, "需第二篇基础",
     "一个 5MB 的 String 能卡住整个实例：大 key 的定义、redis-cli --bigkeys、SCAN 分批删除与拆分方案。"),
    (18, 2, "热 key：发现与打散", "018_第18章_热key发现与打散.html", 30, "需第二篇基础",
     "流量都打到一个 key 上怎么办：--hotkeys、MONITOR 的代价、本地缓存+随机后缀的打散组合拳。"),
    (19, 2, "内存碎片与整理", "019_第19章_内存碎片与整理.html", 30, "需第二篇基础",
     "mem_fragmentation_ratio 高就是坏事吗？activedefrag 的原理与代价、什么时候该重启而不是硬整理。"),
    (20, 2, "持久化方案设计实验", "020_第20章_持久化方案设计实验.html", 35, "需第二篇基础",
     "三个角色（纯缓存/可容忍少量丢失/不能丢）三套方案：动手完成一次从配置到验证的完整持久化设计。"),

    (21, 3, "Cache-Aside 读写模板", "021_第21章_Cache-Aside读写模板.html", 35, "需第一、二篇基础",
     "缓存三问的总纲：旁路缓存的读写两段伪代码、命中率怎么算、为什么 90% 的业务用它就够了。"),
    (22, 3, "更新策略：为什么是删不是改", "022_第22章_更新策略为什么是删不是改.html", 30, "需第三篇第 21 章基础",
     "更新缓存 vs 删除缓存、先删缓存 vs 先改库——四个选项里只有一个是对的，推演给你看。"),
    (23, 3, "缓存穿透：空值与布隆过滤器", "023_第23章_缓存穿透空值与布隆过滤器.html", 35, "需第三篇基础",
     "查不存在的数据把 DB 打挂：空值缓存的 TTL 设计、布隆过滤器的误判率账、接口层校验兜底。"),
    (24, 3, "缓存击穿：互斥与逻辑过期", "024_第24章_缓存击穿互斥与逻辑过期.html", 35, "需第三篇基础",
     "热点 key 过期瞬间的惊群：互斥锁重建与逻辑过期两条路线的完整代码与取舍。"),
    (25, 3, "缓存雪崩：TTL 抖动与高可用", "025_第25章_缓存雪崩TTL抖动与高可用.html", 30, "需第三篇基础",
     "大量 key 同时失效或 Redis 宕机：TTL 加随机值、多级兜底、熔断降级——让雪崩止于设计阶段。"),
    (26, 3, "缓存与 DB 一致性推演", "026_第26章_缓存与DB一致性推演.html", 35, "需第三篇基础",
     "为什么强一致在缓存体系里是伪命题：三种异常时序逐一推演，给出工程上『最终一致』的务实边界。"),
    (27, 3, "延迟双删的正确姿势", "027_第27章_延迟双删的正确姿势.html", 30, "需第三篇第 26 章基础",
     "延迟双删不是银弹：它的适用场景、延时时长怎么定、为什么读写分离下它才真正有意义。"),
    (28, 3, "binlog 订阅同步方案", "028_第28章_binlog订阅同步方案.html", 35, "需第三篇基础",
     "把删缓存的责任从业务代码剥离：Canal 订阅 binlog → 消息队列 → 删缓存的完整链路与重试设计。"),
    (29, 3, "团队缓存规范模板", "029_第29章_团队缓存规范模板.html", 30, "需第三篇基础",
     "把前八章沉淀成一页纸：key 命名、TTL 分级、必加的三大防护、Code Review 缓存检查清单。"),
    (30, 3, "多级缓存：本地+分布式", "030_第30章_多级缓存本地加分布式.html", 35, "需第三篇基础",
     "Caffeine/Guava 在前、Redis 在后：多级缓存的失效同步难题、短 TTL 的自愈思想、什么时候值得上两级。"),
    (31, 3, "缓存监控与命中率优化", "031_第31章_缓存监控与命中率优化.html", 30, "需第三篇基础",
     "keyspace_hits/misses、hit_rate、evicted_keys：看懂 INFO 里的缓存体检单，把命中率从 70% 拉到 95%。"),
    (32, 3, "案例：商品详情缓存全链路", "032_第32章_案例商品详情缓存全链路.html", 35, "需第三篇基础",
     "第三篇收官战：从商品详情页出发，把穿透/击穿/雪崩/一致性四道防线完整落到一个方案里。"),

    (33, 4, "为什么需要分布式锁", "033_第33章_为什么需要分布式锁.html", 30, "需前三篇基础",
     "synchronized 管不了三台机器：从超卖问题出发，理解分布式锁要解决的『互斥+容错+可重入』三件事。"),
    (34, 4, "SETNX 与锁的基本实现", "034_第34章_SETNX与锁的基本实现.html", 35, "需第四篇第 33 章基础",
     "从 setnx 的坑到 SET NX EX 的正确姿势：锁值为什么要用唯一标识、释放为什么必须用 Lua。"),
    (35, 4, "锁续期与看门狗", "035_第35章_锁续期与看门狗.html", 35, "需第四篇第 34 章基础",
     "业务没跑完锁先过期怎么办：Redisson 看门狗的续期原理、手写续期线程的完整实现。"),
    (36, 4, "RedLock 争议与取舍", "036_第36章_RedLock争议与取舍.html", 30, "需第四篇基础",
     "Martin Kleppmann 与 antirez 的世纪之争：RedLock 的算法流程、被批在哪里、工程上该不该用。"),
    (37, 4, "Lua 脚本：真正的原子组合", "037_第37章_Lua脚本真正的原子组合.html", 35, "需第四篇基础",
     "把多条命令打包成一次原子执行：EVAL 语法、KEYS/ARGV 约定、脚本缓存的 EVALSHA 与三个注意事项。"),
    (38, 4, "计数与限流器实现", "038_第38章_计数与限流器实现.html", 35, "需第四篇基础",
     "固定窗口、滑动窗口、令牌桶三种限流器的 Redis 实现与边界缺陷，附 Lua 完整代码。"),
    (39, 4, "排行榜：ZSet 进阶用法", "039_第39章_排行榜ZSet进阶用法.html", 30, "需第一篇第 8 章基础",
     "周榜/总榜/并列名次/分数并列的时间戳技巧：ZSet 排行榜工程化全部细节。"),
    (40, 4, "延迟队列：ZSet 方案", "040_第40章_延迟队列ZSet方案.html", 35, "需第四篇基础",
     "订单 15 分钟未支付自动取消：score 存执行时间的 ZSet 延迟队列，与 RabbitMQ/Redisson 方案对比。"),
    (41, 4, "分布式会话与单点登录配合", "041_第41章_分布式会话与单点登录配合.html", 30, "需第四篇基础",
     "登录态为什么搬进 Redis：Session 共享、Token+TTL 滑动续期、踢人下线与单点登出的实现。"),
    (42, 4, "案例：秒杀系统设计", "042_第42章_案例秒杀系统设计.html", 40, "需第四篇基础",
     "第四篇收官战：预热库存、Lua 原子扣减、限流削峰、MQ 异步落库——一个能扛住瞬时洪峰的秒杀方案。"),

    (43, 5, "主从复制原理与搭建", "043_第43章_主从复制原理与搭建.html", 35, "需前四篇基础",
     "全量同步与增量同步的分水岭：replication id 与 offset、repl_backlog、动手搭一主两从。"),
    (44, 5, "哨兵：自动故障切换", "044_第44章_哨兵自动故障切换.html", 35, "需第五篇第 43 章基础",
     "主库挂了谁来兜底：哨兵的三大任务、客观下线与主观下线、一次完整的故障切换时间线。"),
    (45, 5, "哨兵选主与通知机制", "045_第45章_哨兵选主与通知机制.html", 30, "需第五篇第 44 章基础",
     "哨兵怎么选新主（四条优先级）与哨兵之间怎么选Leader：Raft 式协商、通知客户端的 pub/sub 频道。"),
    (46, 5, "Cluster 概念：分片世界", "046_第46章_Cluster概念分片世界.html", 35, "需第五篇基础",
     "16384 个 slot 怎么分数据：哈希槽与一致性哈希的区别、为什么是 16384、Gossip 协议入门。"),
    (47, 5, "slot 与路由：moved/ask", "047_第47章_slot与路由moved和ask.html", 35, "需第五篇第 46 章基础",
     "客户端怎么知道 key 在哪个节点：MOVED 与 ASK 的区别、smart client 的 slot 缓存、hash tag 限制多 key 命令。"),
    (48, 5, "Cluster 运维与扩容", "048_第48章_Cluster运维与扩容.html", 35, "需第五篇基础",
     "cluster meet/addslots/reshard 实操：扩容迁移期间请求会怎样、节点下线与故障恢复的完整流程。"),
    (49, 5, "客户端适配与注意事项", "049_第49章_客户端适配与注意事项.html", 30, "需第五篇基础",
     "Lettuce/Jedis/go-redis 在 Cluster 下的行为差异：拓扑刷新、pipeline 限制、事务与 Lua 的 slot 约束。"),
    (50, 5, "管道、事务与脚本的性能账", "050_第50章_管道事务与脚本的性能账.html", 35, "需第五篇基础",
     "RTT 是隐形杀手：pipeline 提速 10 倍的原理、MULTI/EXEC 与 Lua 的区别、三者怎么选怎么混用。"),
    (51, 5, "性能压测：redis-benchmark", "051_第51章_性能压测redis-benchmark.html", 30, "需第五篇基础",
     "用官方工具压出真实基线：常用参数组合、压测报告怎么读、延迟毛刺的排查路径（LATENCY/慢日志）。"),
    (52, 5, "常见故障复盘五例", "052_第52章_常见故障复盘五例.html", 35, "需第五篇基础",
     "五个真实事故现场：fork 卡顿、KEYS 打挂、主从切换丢数据、大 key 阻塞、带宽打满——每个都给检查清单。"),
    (53, 5, "安全：ACL 与网络隔离", "053_第53章_安全ACL与网络隔离.html", 30, "需第五篇基础",
     "FLUSHALL 加一个空密码等于裸奔：requirepass、Redis 6 ACL 用户体系、bind/防火墙/危险命令改名。"),
    (54, 5, "面试知识体系梳理与延伸路线", "054_第54章_面试知识体系梳理与延伸路线.html", 40, "全书完",
     "全书收官：把 54 章压缩成一张面试知识网——高频 30 问自查、项目话术模板、后续延伸路线图。"),
]

TOP_NAV = ('<nav class="doc-nav top" aria-label="文档导航">\n'
           '  <a class="doc-nav-btn" href="../../00_目录.html">📖 全书目录</a>\n'
           '  <a class="doc-nav-btn home" href="../../../index.html">⌂ 返回首页</a>\n'
           '{prev}{next}</nav>\n')

BOTTOM = ('</main>\n</div>\n'
          '<nav class="doc-nav bottom">\n'
          '  <a class="doc-nav-btn" href="../../00_目录.html">📖 全书目录</a>\n'
          '  <a class="doc-nav-btn home" href="../../../index.html">⌂ 返回首页</a>\n'
          '{prev}{next}</nav>\n'
          '<footer>从 0 到精通 · 《Redis 从 0 到精通》 · 第 {num} 章 {title}</footer>\n'
          '<button id="backTop" type="button" aria-label="回到顶部">↑</button>\n'
          '{scripts}</body>\n</html>\n')


def build():
    n = len(CHAPTERS)
    ok, errs = 0, []
    for idx, (num, part, title, fname, minutes, level, desc) in enumerate(CHAPTERS):
        frag_path = os.path.join(FRAG, "c%03d.html" % num)
        if not os.path.isfile(frag_path):
            errs.append("missing frag: %s" % frag_path)
            continue
        body = open(frag_path, encoding="utf-8").read().rstrip() + "\n"
        pdir = PART_DIR[part]
        out = os.path.join(ROOT, pdir, fname)
        os.makedirs(os.path.dirname(out), exist_ok=True)

        # nav buttons
        if idx > 0:
            p = CHAPTERS[idx - 1]
            prev_top = '  <a class="doc-nav-btn" href="%s">← 上一章</a>\n' % ("../" + PART_DIR[p[1]] + "/" + p[3] if p[1] != part else p[3])
            prev_bot = prev_top
        else:
            prev_top = '  <a class="doc-nav-btn" href="../../00_目录.html">← 序章</a>\n'
            prev_bot = prev_top
        if idx < n - 1:
            nx = CHAPTERS[idx + 1]
            next_url = "../" + PART_DIR[nx[1]] + "/" + nx[3] if nx[1] != part else nx[3]
            next_top = '  <a class="doc-nav-btn" href="%s">下一章 →</a>\n' % next_url
            next_bot = next_top
        else:
            next_top = '  <a class="doc-nav-btn hidden" href="../../00_目录.html">下一篇 →</a>\n'
            next_bot = next_top

        title_tag = "第 %d 章 %s｜Redis 从 0 到精通" % (num, title)
        head = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                '<title>%s</title>\n%s\n<style>%s%s</style>\n'
                '<link rel="stylesheet" href="../../../glossary/glossary.css">\n'
                '<link rel="stylesheet" href="../../../assets/app.css">\n</head>\n'
                % (title_tag, FAVICON, STYLE, CHAP_CSS))
        hero = ('<header class="hero">\n  <div class="container">\n'
                '    <p class="breadcrumb">从 0 到精通 · 《Redis 从 0 到精通》 · %s</p>\n'
                '    <h1>第 %d 章 %s</h1>\n    <div class="meta-row">\n'
                '      <span class="badge std">教科书</span>\n'
                '      <span class="meta">第 %d 章 / 共 54 章 · 预计 %d 分钟 · %s</span>\n'
                '    </div>\n    <p class="hero-desc">%s</p>\n  </div>\n</header>\n'
                % (PART_NAME[part], num, title, num, minutes, level, desc))
        page = head + hero + (TOP_NAV % {"prev": prev_top, "next": next_top}) + body + \
               (BOTTOM % {"prev": prev_bot, "next": next_bot, "num": num, "title": title, "scripts": SCRIPTS})
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
        ok += 1
    print("built %d/%d chapters" % (ok, n))
    if errs:
        print("\n".join(errs))
        sys.exit(1)


if __name__ == "__main__":
    build()
