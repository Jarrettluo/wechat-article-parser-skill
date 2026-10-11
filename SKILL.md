---
name: wechat-article-parser
description: 微信公众号文章解析技能，用于抓取和总结微信文章内容。当用户提供微信文章链接（mp.weixin.qq.com）或要求解读微信文章时使用此技能。
---

# 微信文章解析

## 概述

用于抓取微信公众号文章的完整内容并总结。支持自动提取文章标题、摘要和正文。

## 使用方法

### 1. 抓取单篇文章

使用 `scripts/parse_wechat_article.py` 脚本：

```bash
python scripts/parse_wechat_article.py <url>
```

示例：
```bash
python scripts/parse_wechat_article.py "https://mp.weixin.qq.com/s/xxx"
```

### 2. 脚本功能

- 自动提取文章标题和摘要
- 从 `window.cgiDataNew.content_noencode` 中解析完整正文
- 输出结构化的文章内容供总结
- 保存 HTML 到本地文件供后续查看

## 输出内容

脚本会输出：
- 文章标题
- 文章摘要
- 正文段落（纯文本）
- 同时保存 `article_full.html` 文件

## 依赖

- Python 3
- requests
- beautifulsoup4

安装依赖：
```bash
pip install requests beautifulsoup4
```
