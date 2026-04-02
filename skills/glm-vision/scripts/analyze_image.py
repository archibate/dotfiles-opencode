#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai",
# ]
# ///
"""
GLM-4.6V 图片分析脚本
使用智谱 GLM-4.6V 多模态模型分析图片

用法:
    python analyze_image.py -i <图片路径或URL> -p <提示词> [-m <模型>] [-d]
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from openai import OpenAI


def load_image_as_base64(image_path: str) -> str:
    """将本地图片转换为 base64 编码"""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def is_url(text: str) -> bool:
    """判断是否为 URL"""
    return text.startswith("http://") or text.startswith("https://")


def analyze_image(
    image_source: str,
    prompt: str,
    model: str = "glm-4.6v-flash",
    detail: bool = False,
    api_key: str | None = None,
) -> str:
    """
    使用 GLM-4.6V 分析图片

    Args:
        image_source: 图片路径或 URL
        prompt: 分析提示词
        model: 模型名称
        detail: 是否启用详细思考模式
        api_key: API Key（如未提供则从环境变量读取）

    Returns:
        分析结果文本
    """
    # 获取 API Key
    key = api_key or os.environ.get("ZHIPU_API_KEY")
    if not key:
        raise ValueError(
            "未设置 ZHIPU_API_KEY 环境变量，请设置后重试:\n"
            "  export ZHIPU_API_KEY='your-api-key'"
        )

    # 初始化客户端
    client = OpenAI(
        api_key=key,
        base_url="https://open.bigmodel.cn/api/paas/v4",
    )

    # 准备图片数据
    if is_url(image_source):
        image_url = image_source
    else:
        image_url = load_image_as_base64(image_source)

    # 构建消息
    content = [
        {"type": "image_url", "image_url": {"url": image_url}},
        {"type": "text", "text": prompt},
    ]

    # 构建请求参数
    request_params = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
    }

    # 启用思考模式
    if detail:
        request_params["thinking"] = {"type": "enabled"}

    # 发送请求
    try:
        response = client.chat.completions.create(**request_params)
        return response.choices[0].message.content
    except Exception as e:
        return f"分析失败: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="使用 GLM-4.6V 分析图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析本地图片
  python analyze_image.py -i photo.jpg -p "描述这张图片"

  # 分析 URL 图片
  python analyze_image.py -i https://example.com/image.jpg -p "这是什么?"

  # 使用详细模式
  python analyze_image.py -i screenshot.png -p "分析这个界面" -d

  # 指定模型
  python analyze_image.py -i image.png -p "OCR提取文字" -m glm-4.6v
        """,
    )

    parser.add_argument(
        "-i", "--image",
        required=True,
        help="图片路径或 URL",
    )

    parser.add_argument(
        "-p", "--prompt",
        required=True,
        help="分析提示词",
    )

    parser.add_argument(
        "-m", "--model",
        default="glm-4.6v-flash",
        choices=["glm-4.6v-flash", "glm-4.6v", "glm-4.6v-flashx"],
        help="模型名称 (默认: glm-4.6v-flash 免费版)",
    )

    parser.add_argument(
        "-d", "--detail",
        action="store_true",
        help="启用详细思考模式",
    )

    parser.add_argument(
        "-k", "--api-key",
        help="API Key (如未提供则从 ZHIPU_API_KEY 环境变量读取)",
    )

    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="以 JSON 格式输出结果",
    )

    args = parser.parse_args()

    # 执行分析
    result = analyze_image(
        image_source=args.image,
        prompt=args.prompt,
        model=args.model,
        detail=args.detail,
        api_key=args.api_key,
    )

    # 输出结果
    if args.json:
        output = {
            "image": args.image,
            "prompt": args.prompt,
            "model": args.model,
            "result": result,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(result)


if __name__ == "__main__":
    main()
