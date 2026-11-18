# -*- coding:utf-8 -*-
"""
打 call 应援箱。运行后打开 http://127.0.0.1:5000 。
填完爱豆和粉丝，按「装进箱子」，舞台上的海报和灯牌一起出来。
业务函数在 services.py。不要把钥匙写进这个文件。
"""
import json
import os
import sys
import wave

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from flask import Flask, jsonify, render_template, request

import services

app = Flask(__name__)
_HERE = os.path.dirname(os.path.abspath(__file__))
_BOARD = os.path.join(_HERE, "data", "board.json")
_STATIC = os.path.join(_HERE, "static")

_SEED = [
    {"fan": "小美", "score": 140},
    {"fan": "阿杰", "score": 85},
    {"fan": "大熊", "score": 50},
    {"fan": "小林", "score": 160},
]


def clean(obj):
    if obj is Ellipsis:
        return None
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [clean(x) for x in obj]
    return obj


def load_board():
    try:
        with open(_BOARD, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            return data
    except (OSError, json.JSONDecodeError):
        pass
    save_board(_SEED)
    return list(_SEED)


def save_board(board):
    os.makedirs(os.path.dirname(_BOARD), exist_ok=True)
    with open(_BOARD, "w", encoding="utf-8") as f:
        json.dump(board, f, ensure_ascii=False, indent=2)


def _call(name, *args, **kwargs):
    fn = getattr(services, name, None)
    if not callable(fn):
        return None
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        print("这里出错了（" + name + "）：", type(e).__name__, e)
        return None


def _pack(board, idol, style, extras, prefix, by):
    ranked = _call("sort_board", board, by)
    if not isinstance(ranked, list):
        ranked = list(board)
    cards = []
    for i, fan in enumerate(ranked, 1):
        card = _call("fan_to_card", fan, i, style, extras, prefix)
        if isinstance(card, dict) and card.get("fan"):
            cards.append(card)
    poster = _call("make_poster", idol, ranked, style, top=30, extras=extras, prefix=prefix)
    scores_raw = _call("map_scores", board)
    scored = isinstance(scores_raw, list)
    scores = scores_raw if scored else []
    tops_raw = _call("top_fans", board, 50)
    has_tops = isinstance(tops_raw, list)
    tops = tops_raw if has_tops else []
    total = 0
    for n in scores:
        if isinstance(n, int):
            total = total + n
    return {
        "cards": clean(cards),
        "poster": poster if isinstance(poster, str) else "",
        "summary": {
            "count": len(board),
            "total": total if scored else None,
            "pass": len(tops) if has_tops else None,
            "tops": clean(tops) if has_tops else None,
        },
    }


@app.route("/")
def index():
    return render_template("index.html", lesson=2)


@app.route("/api/board")
def api_board():
    idol = request.args.get("idol", "小星").strip() or "小星"
    style = request.args.get("style", "热血")
    by = request.args.get("by", "score")
    raw = request.args.get("extras", "").replace("，", ",")
    extras = [w.strip() for w in raw.split(",") if w.strip()]
    prefix = request.args.get("prefix", "").strip()
    return jsonify(_pack(load_board(), idol, style, extras, prefix, by))


@app.route("/api/join", methods=["POST"])
def api_join():
    body = request.get_json(silent=True) or {}
    idol = str(body.get("idol") or "小星").strip() or "小星"
    style = body.get("style") or "热血"
    fan = str(body.get("fan") or "").strip()
    try:
        score = int(body.get("score") or 0)
    except (TypeError, ValueError):
        score = 0
    extras = body.get("extras") or []
    if isinstance(extras, str):
        extras = [w.strip() for w in extras.replace("，", ",").split(",") if w.strip()]
    prefix = str(body.get("prefix") or "")
    by = body.get("by") or "score"
    board = load_board()
    if fan:
        found = False
        for item in board:
            if item.get("fan") == fan:
                item["score"] = score
                found = True
        if not found:
            board.append({"fan": fan, "score": score})
        save_board(board)
    pack = _pack(board, idol, style, extras, prefix, by)
    if not pack["cards"] and not pack["poster"]:
        pack["hint"] = "榜还是空的。先去写 services.py 里的名片和海报。"
    return jsonify(pack)


def _as_wav(path):
    """合成结果是裸 PCM。补上 WAV 头，浏览器才能播。"""
    with open(path, "rb") as f:
        blob = f.read()
    if blob[:4] == b"RIFF":
        return
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(blob)


@app.route("/api/speak", methods=["POST"])
def api_speak():
    body = request.get_json(silent=True) or {}
    text = str(body.get("text") or "").strip()
    if not text:
        return jsonify({"ok": False, "text": "先装进箱子，再喊出来。"})
    os.makedirs(_STATIC, exist_ok=True)
    path = os.path.join(_STATIC, "board.wav")
    ok = _call("speak_board", text, path)
    if ok is True and os.path.isfile(path) and os.path.getsize(path) > 0:
        _as_wav(path)
        return jsonify({"ok": True, "url": "/static/board.wav"})
    return jsonify({"ok": False, "text": "还没念出来。先写 speak_board。钥匙在工程根目录的 .env。"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
