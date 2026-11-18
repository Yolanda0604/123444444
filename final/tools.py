# -*- coding:utf-8 -*-
"""
打 call 应援榜的工具函数。
口号、积分那一行、名片、名次徽章都在这里。网页上的每一张粉丝卡片都会用到。
"""


# 口号。海报上的大字用这一句。附加词和前缀也在这里拼。
def make_slogan(name, style="热血", *extras, **opts):
    """按风格写一句口号。return 字符串，不要 print。

    热血：名字 + "，冲鸭！"
    温柔：名字 + "，要好好的呀～"
    中二：名字 + "，吾辈应援之魂不灭！"
    其他：名字 + "，加油！"

    extras 里有附加词时，接在后面，写成【词1、词2】。
    opts 里如果有 prefix，加在整句最前面。

    对一下：make_slogan("小星") 是「小星，冲鸭！」。
    make_slogan("小星", "热血", "走花路", "大发") 是「小星，冲鸭！【走花路、大发】」。
    make_slogan("小星", "热血", prefix="♥") 是「♥小星，冲鸭！」。
    """
    if style == "热血":
        base = name + "，冲鸭！"
    elif style == "温柔":
        base = name + "，要好好的呀～"
    elif style == "中二":
        base = name + "，吾辈应援之魂不灭！"
    else:
        base = name + "，加油！"
    if extras:
        base = base + "【" + "、".join(extras) + "】"
    if opts.get("prefix"):
        base = opts["prefix"] + base
    print("口号核对：" + base)
    return base


# 积分行。把一位粉丝收成「名字 · 分数 分（评价）」，海报名单用它。
def format_score(fan):
    """把一位粉丝收成一行：名字 · 分数 分（评价）。

    100 分及以上是铁血粉，50 分及以上是中坚粉，大于 0 是新粉，否则是路人粉。
    没有名字就写「匿名」。没有分数就当 0。

    对一下：{"fan": "小美", "score": 140} 得到「小美 · 140 分（铁血粉）」。
    """
    name = fan.get("fan", "匿名") or "匿名"
    score = int(fan.get("score", 0) or 0)
    if score >= 100:
        level = "铁血粉"
    elif score >= 50:
        level = "中坚粉"
    elif score > 0:
        level = "新粉"
    else:
        level = "路人粉"
    line = name + " · " + str(score) + " 分（" + level + "）"
    print("积分核对：" + line)
    return line


# 五行名片。自己不另写积分和口号，去调用 format_score 和 make_slogan。
def fan_card(fan, style="热血"):
    """五行星的名片。热度星必须调用自己算，口号必须调用 make_slogan，积分那一行必须调用 format_score。

    颗数 = 分数 // 20，最多 5 颗。不满 5 颗用 ☆ 补满。140 分是 ★★★★★。0 分是 ☆☆☆☆☆。
    """
    score = int(fan.get("score", 0) or 0)
    full = score // 20
    if full > 5:
        full = 5
    stars = "★" * full + "☆" * (5 - full)
    name = fan.get("fan", "匿名") or "匿名"
    lines = [
        "╔══════ 粉丝名片 ══════╗",
        "  " + format_score(fan),
        "  热度 " + stars,
        "  口号 " + make_slogan(name, style),
        "╚═══════════════════╝",
    ]
    return "\n".join(lines)


# 灯牌上的身份。第 1 名位置写 C位，前三写前排，其余写气氛组。
def rank_tag(rank):
    """名次徽章。第 1 名是 C位，前 3 名是前排，其余是气氛组。"""
    if rank == 1:
        return "C位"
    if rank <= 3:
        return "前排"
    return "气氛组"
