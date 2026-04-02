# GLM-4.6V API 参考文档

## API 端点

```
POST https://open.bigmodel.cn/api/paas/v4/chat/completions
```

## 认证

在请求头中添加 Bearer Token：

```
Authorization: Bearer YOUR_API_KEY
```

## 模型列表

| 模型名称 | 参数量 | 上下文 | 价格 | 说明 |
|---------|--------|--------|------|------|
| `glm-4.6v-flash` | 9B | 128K | 免费 | 轻量免费版 |
| `glm-4.6v-flashx` | 9B | 128K | 付费 | 轻量高速版 |
| `glm-4.6v` | 106B (12B激活) | 128K | 付费 | 旗舰版 |

## 请求格式

### 基础请求

```json
{
  "model": "glm-4.6v-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "图片URL或Base64"
          }
        },
        {
          "type": "text",
          "text": "你的提示词"
        }
      ]
    }
  ]
}
```

### 启用思考模式

```json
{
  "model": "glm-4.6v-flash",
  "messages": [...],
  "thinking": {
    "type": "enabled"
  }
}
```

### 流式输出

```json
{
  "model": "glm-4.6v-flash",
  "messages": [...],
  "stream": true
}
```

## 输入类型

### 1. 图片 URL

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://example.com/image.jpg"
  }
}
```

### 2. 图片 Base64

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/jpeg;base64,/9j/4AAQ..."
  }
}
```

或直接使用 base64 字符串（不带 data URI 前缀）：

```json
{
  "type": "image_url",
  "image_url": {
    "url": "/9j/4AAQ..."
  }
}
```

### 3. 视频 URL

```json
{
  "type": "video_url",
  "video_url": {
    "url": "https://example.com/video.mp4"
  }
}
```

### 4. 文件 URL

```json
{
  "type": "file_url",
  "file_url": {
    "url": "https://example.com/document.pdf"
  }
}
```

## 多图输入

最多支持 5 张图片同时输入：

```json
{
  "content": [
    {"type": "image_url", "image_url": {"url": "图片1"}},
    {"type": "image_url", "image_url": {"url": "图片2"}},
    {"type": "image_url", "image_url": {"url": "图片3"}},
    {"type": "text", "text": "比较这些图片的异同"}
  ]
}
```

## 响应格式

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "glm-4.6v-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "图片分析结果..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 200,
    "total_tokens": 300
  }
}
```

## 流式响应

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion.chunk",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": "部分内容..."
      },
      "finish_reason": null
    }
  ]
}
```

## 思考模式响应

启用 `thinking` 后，流式响应包含 `reasoning_content`：

```json
{
  "choices": [
    {
      "delta": {
        "reasoning_content": "思考过程...",
        "content": "最终回答..."
      }
    }
  ]
}
```

## 错误响应

```json
{
  "error": {
    "code": "invalid_api_key",
    "message": "API key 无效"
  }
}
```

常见错误码：
- `invalid_api_key`: API Key 无效
- `rate_limit_exceeded`: 请求频率超限
- `invalid_image`: 图片格式不支持
- `context_length_exceeded`: 内容超出上下文限制

## SDK 用法

### Python (openai 兼容)

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

response = client.chat.completions.create(
    model="glm-4.6v-flash",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": "描述这张图片"}
        ]
    }]
)
```

### Python (zhipuai SDK)

```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="YOUR_API_KEY")

response = client.chat.completions.create(
    model="glm-4.6v-flash",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": "描述这张图片"}
        ]
    }]
)
```

## 使用限制

| 用户等级 | 并发数 |
|---------|--------|
| V0 (免费) | 5 |
| V1 | 15 |
| V2 | 30 |
| V3 | 40 |

## 最佳实践

1. **图片大小**: 建议小于 10MB，过大会增加延迟
2. **使用免费模型**: 日常使用 `glm-4.6v-flash` 即可
3. **思考模式**: 复杂分析任务启用 `thinking` 模式
4. **错误处理**: 实现重试逻辑处理临时错误
5. **缓存结果**: 相同图片的重复分析可缓存结果
