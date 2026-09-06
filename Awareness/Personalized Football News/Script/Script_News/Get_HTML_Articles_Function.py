import requests
from bs4 import BeautifulSoup


def get_html_articles(source_name, source_url):

    articles = []

    response = requests.get(
        source_url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    seen_urls = set()

    for a in soup.find_all("a", href=True):

        title = a.get_text(" | ", strip=True)

        if "|" in title:
            title = title.split("|")[-1].strip()

        print(title)

        href = a["href"]

        if len(title) < 15:
            continue

        if "/nyheder/" not in href:
            continue

        if href.startswith("/"):

            href = source_url.rstrip("/") + href

        if href in seen_urls:
            continue

        seen_urls.add(href)

        articles.append({
            "title": title,
            "url": href,
            "source": source_name
        })

    return articles