# -*- coding:utf-8 -*-
"""
mock.py — 本地演示兜底：没钥匙、断网或强制开关时返回预置结果。
对外调用仍走同一套函数名，页面上能继续演示。
"""
import math
import os
import struct

# ---------- 触发开关 ----------

def forced():
    """环境变量 IFLYTEK_MOCK=1 时强制走本地演示。"""
    return os.environ.get("IFLYTEK_MOCK") == "1"

# ---------- 预置数据 ----------
MOCK_STT_TEXT = "夸夸我，今天也要加油哦"
MOCK_OCR_TEXT = "初音未来 手办 售价 168 元 货号 XXX001 系列 VOCALOID"
MOCK_TRANS_TEXT = "Hatsune Miku"
MOCK_TRANS_DICT = {
    "初音未来": "Hatsune Miku",
    "手办": "figure",
    "谷子": "merch",
    "你好": "Hello",
    "再见": "Goodbye",
}
MOCK_FACE_SCORE = 86.5
MOCK_SPARK_TEXT = "今日小票已经打好。中杯 12 元，大杯 15 元，珍珠再加 3 元。"

def translate_fallback(text):
    """用内置小词典翻译；翻不到就原样交回。"""
    for k, v in MOCK_TRANS_DICT.items():
        if k in text:
            return v
    return text

# ---------- MOCK 音频（真实可播的一小段"滴"声） ----------

def mock_pcm(save_path, seconds=0.6):
    """写出一段可播放的短 PCM 到指定路径，交回 True。"""
    rate = 16000
    n = int(rate * seconds)
    freq = 660.0
    frames = bytearray()
    for i in range(n):
        t = i / rate
        env = 1.0 - (i / n) ** 2            # 渐弱包络，避免爆音
        v = int(12000 * env * math.sin(2 * math.pi * freq * t))
        frames += struct.pack("<h", v)
    with open(save_path, "wb") as f:
        f.write(bytes(frames))
    return True

def say_fallback(text, save_path):
    """语音合成兜底：写出模拟短音到指定路径。"""
    return mock_pcm(save_path)
