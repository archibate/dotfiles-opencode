import argparse
import json
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")

def get_headers(use_json=True):
    headers = {}
    if JINA_API_KEY:
        headers["Authorization"] = f"Bearer {JINA_API_KEY}"
    if use_json:
        # Request structured JSON output
        headers["X-Return-Format"] = "json"
    return headers

def read_url(url):
    # Jina Reader API structure: prefix the target URL
    target_url = f"https://r.jina.ai/{url}"
    headers = get_headers(use_json=True)

    try:
        response = requests.get(target_url, headers=headers)
        response.raise_for_status()

        data = response.json().get('data', {})
        return {
            "title": data.get("title", "Untitled"),
            "url": data.get("url", url),
            "content_markdown": data.get("content", "")
        }

    except requests.exceptions.RequestException as e:
        print(f"Error during Jina Reader request: {e}", file=sys.stderr)
        sys.exit(1)

def search_web(query):
    # Jina Search API endpoint
    target_url = "https://s.jina.ai/search"
    params = {"q": query}
    headers = get_headers(use_json=True)

    try:
        response = requests.get(target_url, headers=headers, params=params)
        response.raise_for_status()

        results = []
        data = response.json().get('data', [])

        for item in data:
            results.append({
                "title": item.get("title", "Untitled"),
                "url": item.get("url", ""),
                "content_markdown": item.get("content", "")
            })

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error during Jina Search request: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use Jina AI tools (Reader and Search).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Read parser
    read_parser = subparsers.add_parser("read", help="Convert a URL to Markdown.")
    read_parser.add_argument("url", help="The URL to read.")

    # Search parser
    search_parser = subparsers.add_parser("search", help="Search the web and return Markdown results.")
    search_parser.add_argument("query", help="The search query.")

    args = parser.parse_args()

    result = None
    if args.command == "read":
        result = read_url(args.url)
    elif args.command == "search":
        result = search_web(args.query)

    if result:
        print(json.dumps(result, indent=2))
