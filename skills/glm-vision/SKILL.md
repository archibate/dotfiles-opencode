---
name: glm-vision
description: This skill should be used when the user sends an image and asks to "analyze this image", "describe this picture", "what's in this image", or any request requiring visual understanding of images. Provides image analysis using Zhipu GLM-4.6V multimodal model.
version: 0.1.0
---

# GLM Vision - 图片分析技能

## 概述

使用智谱 GLM-4.6V 多模态模型分析图片内容。支持：
- 图片内容描述和理解
- 图片中的文字提取（OCR）
- 图片元素识别和分析
- 多图对比分析
- 视频内容理解

## 使用场景

当用户发送图片并提出以下类型问题时触发：
- "这张图片里有什么？"
- "请描述这张图片"
- "分析这个截图"
- "这是什么？"
- "图片里的文字是什么？"
- "比较这两张图片"

## API 配置

### 环境变量

需要设置 `ZHIPU_API_KEY` 环境变量：

```bash
export ZHIPU_API_KEY="your-api-key-here"
```

或者在 `~/.claude/settings.json` 中配置：

```json
{
  "env": {
    "ZHIPU_API_KEY": "your-api-key-here"
  }
}
```

### 模型选择

| 模型 | 用途 | 价格 |
|------|------|------|
| `glm-4.6v-flash` | 免费版，日常使用 | 免费 |
| `glm-4.6v` | 旗舰版，复杂推理 | 付费 |
| `glm-4.6v-flashx` | 轻量高速版 | 付费 |

默认使用 `glm-4.6v-flash` 免费模型。

## 调用方式

### 方式一：使用辅助脚本（推荐）

```bash
python3 ~/.claude/skills/glm-vision/scripts/analyze_image.py \
  --image "/path/to/image.jpg" \
  --prompt "请描述这张图片" \
  [--model "glm-4.6v-flash"]
```

参数说明：
- `--image` / `-i`: 图片路径（支持 URL 或本地文件）
- `--prompt` / `-p`: 分析提示词
- `--model` / `-m`: 模型名称（可选，默认免费版）
- `--detail` / `-d`: 启用详细思考模式

### 方式二：直接 API 调用

```python
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

# 读取本地图片
with open("image.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="glm-4.6v-flash",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": img_base64}},
            {"type": "text", "text": "请描述这张图片"}
        ]
    }]
)
print(response.choices[0].message.content)
```

### 方式三：URL 图片

```python
response = client.chat.completions.create(
    model="glm-4.6v-flash",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
            {"type": "text", "text": "分析这张图片"}
        ]
    }]
)
```

## 工作流程

1. **接收图片**: 用户发送图片，保存到临时目录
2. **构建请求**: 将图片转为 base64 或使用 URL
3. **调用 API**: 发送到 GLM-4.6V 模型
4. **返回结果**: 解析并展示分析结果

## 支持的图片格式

- JPEG / JPG
- PNG
- GIF（静态）
- WebP
- BMP

## 示例用法

### 基础图片描述

```bash
python3 ~/.claude/skills/glm-vision/scripts/analyze_image.py \
  -i "/tmp/screenshot.png" \
  -p "描述这张截图的内容"
```

### 详细分析

```bash
python3 ~/.claude/skills/glm-vision/scripts/analyze_image.py \
  -i "/tmp/photo.jpg" \
  -p "分析这张图片的构图、色彩和主题" \
  --detail
```

### OCR 文字提取

```bash
python3 ~/.claude/skills/glm-vision/scripts/analyze_image.py \
  -i "/tmp/document.png" \
  -p "提取图片中的所有文字，保持原有格式"
```

### URL 图片分析

```bash
python3 ~/.claude/skills/glm-vision/scripts/analyze_image.py \
  -i "https://example.com/image.jpg" \
  -p "这张图片展示的是什么？"
```

## 注意事项

1. **API Key 安全**: 不要在代码中硬编码 API Key
2. **图片大小**: 建议图片小于 10MB，过大的图片会增加延迟
3. **网络连接**: 需要稳定的网络访问智谱 API
4. **并发限制**: 免费用户并发数为 5

## 参考资源

- `references/api-reference.md` - 完整 API 参考文档
- `scripts/analyze_image.py` - 图片分析辅助脚本
