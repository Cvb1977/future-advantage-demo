import json
import feedparser
from datetime import datetime
from pathlib import Path

from Get_HTML_Articles_Function import get_html_articles

# ==================================================
# FILER
# ==================================================

PROFILE_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness\Personalized Football News"
    r"\Script\Script_Profil\football_profile.json"
)

HTML_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness\Personalized Football News"
    r"\Script\Script_News\index.html"
)

SOURCES_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness"
    r"\Personalized Football News\\Script\Sources\sources.json"
)


# ==================================================
# HENT PROFIL
# ==================================================

with open(PROFILE_FILE, "r", encoding="utf-8") as f:
    profile = json.load(f)

with open(SOURCES_FILE, "r", encoding="utf-8") as f:
    sources = json.load(f)

interest_words = {}

for category in [
    "teams",
    "competitions",
    "topics",
    "keywords"
]:
    for word, score in profile.get(category, {}).items():

        if word not in interest_words:
            interest_words[word] = 0

        interest_words[word] += score

# ==================================================
# HENT NYHEDER
# ==================================================

articles = []

for source in sources:

    source_name = source["name"]
    source_type = source["type"]
    source_url = source["url"]

    print()
    print("Kilde:", source_name)
    print("Type :", source_type)

    # RSS KILDER
    if source_type == "rss":

        feed = feedparser.parse(source_url)

        print("Artikler fundet:", len(feed.entries))

        for entry in feed.entries:

            title = entry.get("title", "")
            link = entry.get("link", "")

            text = title.lower()

            score = 0
            matched_words = []

            for word, weight in interest_words.items():

                if word.lower() in text:

                    score += weight
                    matched_words.append(word)

            articles.append({
                "title": title,
                "url": link,
                "score": round(score, 2),
                "matches": matched_words
            })
            print(title)

    # HTML KILDER
    elif source_type == "html":

        html_articles = get_html_articles(
            source_name,
            source_url
        )

        print("Artikler fundet:", len(html_articles))

        for article in html_articles:

            title = article["title"]
            link = article["url"]

            text = title.lower()

            score = 0
            matched_words = []

            for word, weight in interest_words.items():

                if word.lower() in text:

                    score += weight
                    matched_words.append(word)

            articles.append({
                "title": title,
                "url": link,
                "score": round(score, 2),
                "matches": matched_words
            })

# ==================================================
# FJERN DUBLETTER
# ==================================================

seen_titles = set()
unique_articles = []

for article in articles:

    title_key = (
    article["title"]
    .lower()
    .replace("-", "")
    .replace(":", "")
)

    if title_key in seen_titles:
        continue

    seen_titles.add(title_key)
    unique_articles.append(article)

articles = unique_articles

# ==================================================
# SORTÉR
# ==================================================

print()
print("Antal artikler efter dublet-fjernelse:", len(articles))
print()

for article in articles[:5]:
    print(article["title"])

articles.sort(
    key=lambda x: x["score"],
    reverse=True
)

print()
print("TOP 10 EFTER SCORING")
print("-" * 80)

for article in articles[:10]:

    print(
        f"Score: {article['score']:.2f}"
    )

    print(
        article["title"]
    )

    print()

top100 = articles[:100]
print()
print("TOP 100 SOM SENDES TIL HTML")
print("-" * 50)

for article in top100:
    print(article["title"])

# ==================================================
# HTML
# ==================================================

updated = datetime.now().strftime(
    "%d-%m-%Y %H:%M"
)

html = f"""
<!DOCTYPE html>
<html lang="da">

<head>

<meta charset="utf-8">

<title>Personalized Football News</title>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 1000px;
    margin: 40px auto;
    background: #f4f4f4;
}}

.news-list {{
    padding-left: 25px;
}}

.news-list li {{
    margin-bottom: 10px;
}}

.news-list a {{
    color: #003366;
    text-decoration: none;
    font-size: 20px;
    font-weight: bold;
}}

.news-list a:hover {{
    text-decoration: underline;
}}
``

.score {{
    color: green;
    font-weight: bold;
}}

.matches {{
    color: #666;
}}

</style>

</head>

<body>

<h1>⚽ Personalized Football News</h1>

<p>
Sidst opdateret:
{updated}
</p>

"""

for i, article in enumerate(top100, start=1):

    html += f"""
    <div class="card">

        <!-- <h2>{i}. {article['title']}</h2> -->
        <h2>
            <a href="{article['url']}" target="_blank">
                {article['title']}
            </a>
        </h2>
        
    </div>
    """

html += """
</body>
</html>
"""

with open(
    HTML_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(html)

print()
print("Nyhedsside opdateret:")
print(HTML_FILE)
print()