# iflytek_kit（本课裁剪版：语音合成 + 星火大模型）

本工程只带当前项目用到的两项能力，其余能力后续课次再发：

| 函数 | 作用 |
| --- | --- |
| `tts_say(text, save_path=...)` | 语音合成：文字 → 语音文件 |
| `spark_chat(prompt)` | 星火大模型：提示词 → 回复文本 |

## 配置凭证（可选）

在任一上层目录放 `.env`，配好后自动走真实 API；不配也能跑，自动走 MOCK 演示模式：

```
IFLYTEK_TTS_APPID=...
IFLYTEK_TTS_API_KEY=...
IFLYTEK_TTS_API_SECRET=...
IFLYTEK_SPARK_APPID=...
IFLYTEK_SPARK_API_KEY=...
IFLYTEK_SPARK_API_SECRET=...
```

- `IFLYTEK_MOCK=1` 可强制 MOCK。
- 真实调用需 `pip install websocket-client requests`；没装不影响 MOCK。

## 目录说明

`core_*` 是真实 API 内核，`client.py` 统一管凭证和 MOCK 判断，`mock.py` 是兜底数据，`auth.py` 是签名工具（后面自己封装时参照）。
