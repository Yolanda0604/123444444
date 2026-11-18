# -*- coding:utf-8 -*-
"""
打 call 应援箱 · 第2课参考写法。
网页上改爱豆、口气、句尾和句首，海报大字会跟着变。填粉丝和分数，按「装进箱子」，名单和灯牌一起出来。
口号、积分、名片、徽章在 tools.py。这里写海报、排序、播报。
不要改 app.py。
"""
from tools import fan_card, format_score, make_slogan, rank_tag
from iflytek_kit import tts_say


# 整张海报。第 2 行是爱豆口号，下面是粉丝积分行。舞台左边显示这段字。
def make_poster(idol, fans, style="热血", **opts):
    """整张榜的海报。第 2 行必须调用 make_slogan，名单每一行必须调用 format_score。

    风格不是热血、温柔、中二时，改成热血，最后多一行提示。
    只取前 top 人。top 用 opts.get("top", 3)。
    按 fans 现在的顺序，不要在这里再排序。
    """
    warn = ""
    if style not in ("热血", "温柔", "中二"):
        warn = "没有「" + style + "」风格，已用热血代替"
        style = "热血"
    top = opts.get("top", 3)
    words = opts.get("extras") or []
    prefix = opts.get("prefix") or ""
    lines = [
        "══ " + idol + " 专场应援海报 ══",
        make_slogan(idol, style, *words, prefix=prefix),
        "—— 到场粉丝名单 ——",
    ]
    for fan in fans[:top]:
        lines.append("  " + format_score(fan))
    if warn:
        lines.append(warn)
    print("海报核对：" + idol + " 共" + str(len(lines)) + "行")
    return "\n".join(lines)


# 一块灯牌要用的数据。名字、声量、星星、口号、身份都收在这个字典里。
def fan_to_card(fan, rank, style="热血", extras=None, prefix=""):
    """把一位粉丝收成网页上的一张卡片。积分行、口号、徽章都要调用已经写好的函数。"""
    name = fan.get("fan", "匿名") or "匿名"
    score = int(fan.get("score", 0) or 0)
    stars = score // 20
    if stars > 5:
        stars = 5
    extras = extras or []
    card = {
        "fan": name,
        "score": score,
        "line": format_score(fan),
        "stars": stars,
        "slogan": make_slogan(name, style, *extras, prefix=prefix),
        "tag": rank_tag(rank),
        "card": fan_card(fan, style),
    }
    print("卡片已生成：" + name + "（" + card["tag"] + "）")
    return card


# 灯牌从左到右的顺序。按声量、星星颗数或名字长短重排，不改原来的名单。
def sort_board(board, by="score"):
    """按积分、名字字数或星级排出新列表。不要改原来的 board。

    by 是 score：按分数从高到低。
    by 是 name：按名字字数从少到多。
    by 是 star：按 score // 20 从高到低。
    """
    score = lambda fan: int(fan.get("score", 0) or 0)
    if by == "name":
        return sorted(board, key=lambda fan: len(fan.get("fan", "")))
    if by == "star":
        return sorted(board, key=lambda fan: score(fan) // 20, reverse=True)
    return sorted(board, key=score, reverse=True)


# 达标的粉丝名字。声量达到指定分数的才留下。
def top_fans(board, min_score=50):
    """留下分数达到 min_score 的粉丝名字。用 filter，外面套成列表。"""
    enough = lambda fan: int(fan.get("score", 0) or 0) >= min_score
    names = []
    for fan in filter(enough, board):
        names.append(fan.get("fan", "匿名"))
    return names


# 把每人的声量抽成一串数字，用来加总。
def map_scores(board):
    """抽出所有人的分数。用 map，外面套 list。页面用它算全场总分。"""
    score = lambda fan: int(fan.get("score", 0) or 0)
    return list(map(score, board))


# 把海报交给讯飞念出来。点「喊出来」时用它。
def speak_board(text, save_path):
    """把海报念出来。return tts_say 的结果。"""
    return tts_say(text, save_path=save_path, voice="x4_yezi")
