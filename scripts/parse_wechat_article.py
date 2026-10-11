#!/usr/bin/env python3
"""
微信公众号文章解析脚本
用法: python parse_wechat_article.py <url>
"""

import sys
import requests
import re
from bs4 import BeautifulSoup


def decode_js_escape(s):
    """解码 JavaScript 转义字符（\\xNN 格式）"""
    result = ''
    i = 0
    while i < len(s):
        if s[i:i+2] == '\\x' and i+4 <= len(s):
            hex_val = s[i+2:i+4]
            result += chr(int(hex_val, 16))
            i += 4
        else:
            result += s[i]
            i += 1
    return result


def parse_wechat_article(url):
    """解析微信公众号文章"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"正在获取文章: {url}")
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    # 提取标题
    title = ""
    title_pat = r'title:\s*JsDecode\(\s*\'(.*?)\'\s*\)'
    title_match = re.search(title_pat, response.text)
    if title_match:
        title = decode_js_escape(title_match.group(1))

    # 提取摘要
    desc = ""
    desc_pat = r'desc:\s*JsDecode\(\s*\'(.*?)\'\s*\)'
    desc_match = re.search(desc_pat, response.text)
    if desc_match:
        desc = decode_js_escape(desc_match.group(1))

    # 提取正文内容
    content_html = ""
    content_pat = r'content_noencode:\s*JsDecode\(\s*\'(.*?)\'\s*\)'
    content_match = re.search(content_pat, response.text, re.DOTALL)
    if content_match:
        content_encoded = content_match.group(1)
        content_html = decode_js_escape(content_encoded)
        
        # 保存完整 HTML
        with open('article_full.html', 'w', encoding='utf-8') as f:
            f.write(content_html)
        print("✅ 完整 HTML 已保存到 article_full.html")

    # 输出结果
    print()
    print("=" * 60)
    if title:
        print(f"标题: {title}")
    if desc:
        print(f"摘要: {desc}")
    print("=" * 60)
    print()

    if content_html:
        # 用 BeautifulSoup 提取纯文本
        soup = BeautifulSoup(content_html, 'html.parser')
        paragraphs = soup.find_all(['p', 'section', 'h1', 'h2', 'h3', 'h4', 'li'])
        
        print("=== 文章正文 ===")
        print()
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 3:
                print(text)
                print()
    else:
        print("⚠️ 无法提取文章正文")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python parse_wechat_article.py <微信文章URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    parse_wechat_article(url)
