import json
import feedparser
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


from Get_HTML_Articles_Function import get_html_articles

# ==================================================
# FILER
# ==================================================

PROFILE_FILE = (
    BASE_DIR.parent /
    "Script_Profil" /
    "football_profile.json"
)

HTML_FILE = (
    BASE_DIR.parent.parent /
    "Website" /
    "index.html"
)

SOURCES_FILE = (
    BASE_DIR.parent /
    "Sources" /
    "Sources.json"
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

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background: #f4f4f4;
}}

.hero-header {{
    position: relative;
    width: 100%;
    box-sizing: border-box;
    background: linear-gradient(
        to bottom,
        #000000,
        #8a6a44,
        #d8b07a
    );

    color: white;
    padding: 10px 40px 10px 40px;
}}

.header-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.title-area {{
    flex: 1;
    text-align: center;
}}

.title-area h1 {{
    margin: 0;
    font-size: 56px;
    color: #f0c78a;
}}

.title-area h2 {{
    margin: 0;
    font-size: 34px;
    font-weight: normal;
    color: #f0c78a;
}}

.main-nav {{
    position: absolute;
    bottom: 0;
    left: 0;

    display: flex;
    gap: 0;
}}

.main-nav a {{
    display: block;

    background: #7a6242;
    color: white;

    padding: 12px 25px;

    text-decoration: none;
    font-weight: bold;

    border-top-left-radius: 8px;
    border-top-right-radius: 8px;

    border-right: 1px solid #5d4930;
}}

.main-nav a:hover {{
    background: rgba(255,255,255,0.2);
}}

.main-nav a.active {{
    background: white;
    color: black;
}}

.logo-area {{
    display: flex;
    align-items: center;
    justify-content: flex-end;

    position: relative;
    left: 35px;
    top: 5px;
}}

.logo-area img {{
    height: 140px;
    width: auto;
    margin-right: 0;

}}

.content {{
    max-width: 1000px;
    margin-left: 20px;
    margin-right: auto;
}}

.main-layout {{
    display: flex;
    align-items: flex-start;
}}

.left-column {{
    width: 70%;
}}

.right-column {{
    width: 30%;
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin-left: 20px;
    box-sizing: border-box;
}}


.news-list {{
    padding-left: 025px;
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

<body>

<header class="hero-header">

    <div class="header-content">

        <div class="title-area">
            <h1>Future Advantage</h1>
            <h2>Football Talent Agency</h2>
        </div>

        <nav class="main-nav">
            <a href="index.html">News</a>
            <a href="IndexGoals.html">Goals</a>
            <a href="IndexAgency.html">Agency</a>
        </nav>

        <div class="logo-area">
            <img src="Logo.png" alt="Future Advantage Logo">
        </div>

    </div>
</header>

<div class="main-layout">

    <div class="left-column">

        <div class="content">

            <p>
                Sidst opdateret: {updated}
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
        </div>
    </div>        

    <div class="right-column">
        <h2>Medlemsområde</h2>
        <p>Login kommer her</p>
        <p>Mulighed for at vælge personaliserede nyheder kommer her</p>

        <div class="promo-section">
            <h2>Agency Package Reklame Film</h2>
            <p>Præsentation af services og pakkelæsninger kommer her</p>
        </div>
    </div>

</div>    

        

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