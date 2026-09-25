from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass

import feedparser

from gemini_client import generate

_KEYWORD_PROMPT = """You extract search keywords from a short note so it can
be looked up on Google News.

Read the note and return ONLY a short search phrase (3-5 words) capturing
its core, newsworthy subject - the kind of phrase you'd type into a news
search box. No punctuation beyond spaces, no quotes, no explanation, nothing
else in the response."""

_RSS_ENDPOINT = "https://news.google.com/rss/search"


@dataclass
class NewsItem:
    headline: str
    source: str
    date: str
    link: str
    summary: str


def extract_keywords(thought: str) -> str:
    phrase = generate(_KEYWORD_PROMPT, f"Note:\n\n{thought}", temperature=0.2)
    return phrase.strip().strip('"').strip()


def fetch_top_news(query: str) -> NewsItem | None:
    if not query:
        return None

    url = (
        _RSS_ENDPOINT
        + "?"
        + urllib.parse.urlencode({"q": query, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})
    )
    feed = feedparser.parse(url)
    if not feed.entries:
        return None

    entry = feed.entries[0]
    source = getattr(entry, "source", None)
    source_title = source.get("title", "") if source else ""

    return NewsItem(
        headline=entry.get("title", "").strip(),
        source=source_title.strip(),
        date=entry.get("published", "").strip(),
        link=entry.get("link", "").strip(),
        summary=_strip_html(entry.get("summary", "")).strip(),
    )


def build_verify_footer(item: NewsItem) -> str:
    bar = "_" * 32
    return (
        f"\n\n{bar}\n\n"
        f"NEWS SOURCE: {item.headline}\n"
        f"FROM: {item.source} · {item.date}\n"
        f"LINK: {item.link}\n"
        f"⚠ Check this before publishing – you are the author of this claim\n\n"
        f"{bar}"
    )


def _strip_html(raw: str) -> str:
    return re.sub(r"<[^<]+?>", "", raw)
