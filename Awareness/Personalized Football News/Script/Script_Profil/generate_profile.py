from urllib.parse import urlparse
import feedparser
import requests

import json
import re
from datetime import datetime, timezone
from collections import Counter


# ==================================================
# Tilføj funktion til at bestemme type
# ==================================================


def discover_source_type(domain):

    candidates = [
        f"https://{domain}/rss",
        f"https://{domain}/feed"
    ]

    for candidate in candidates:

        try:

            feed = feedparser.parse(candidate)

            if len(feed.entries) > 0:
                return "rss"

        except:
            pass

    try:

        response = requests.get(
            f"https://{domain}",
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        if response.status_code == 200:
            return "html"

    except:
        pass

    return "unknown"

# ==================================================
# FILER
# ==================================================

JSON_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness"
    r"\Personalized Football News\Safari_Web_History\Historic.json"
)

PROFILE_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness\Personalized Football News"
    r"\Script\Script_Profil\football_profile.json"
)

SOURCES_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness"
    r"\Personalized Football News\Script\Sources\sources.json"
)

# ==================================================
# FODBOLDIDENTIFIKATION
# ==================================================

FOOTBALL_HINTS = [
    "fodbold",
    "superliga",
    "premier",
    "champions",
    "europa league",
    "conference league",
    "football",
    "soccer",
    "transfer",
    "bold.dk",
    "tipsbladet",
    "goal",
    "offside",
    "brøndby",
    "fck",
    "agf",
    "manchester",
    "arsenal",
    "liverpool",
    "chelsea",
    "tottenham",
    "barcelona",
    "real madrid",
]

STOPWORDS = {
    "der", "det", "den", "til", "for", "med", "har",
    "som", "ikke", "fra", "efter", "mod", "ved",
    "kan", "skal", "blev", "bliver", "mere", "mindre",
    "siger", "sagde", "over", "under", "ind", "ud",
    "hos", "om", "på", "af", "en", "et", "de",
    "og", "eller", "er", "var"
}

TOPIC_WORDS = {
    "transfer",
    "transfers",
    "skade",
    "skader",
    "træner",
    "trænere",
    "fyring",
    "angriber",
    "forsvarer",
    "målmand",
    "midtbanespiller",
    "kontrakt",
    "talent",
    "talenter",
    "profil",
    "profiler",
    "køb",
    "salg",
    "udlån"
}

COMPETITIONS = {
    "superliga",
    "premier",
    "champions",
    "europa",
    "conference",
    "bundesliga",
    "laliga",
    "serie"
}

# ==================================================
# INDLÆS HISTORIK
# ==================================================

print("Indlæser historik...")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

history_items = data.get("history", [])

print(f"Historikposter fundet: {len(history_items)}")

# ==================================================
# INTERESSEPROFIL
# ==================================================

keywords = Counter()
teams = Counter()
competitions = Counter()
topics = Counter()
source_scores = Counter()

now = datetime.now(timezone.utc)

football_articles_found = 0

for item in history_items:

    title = item.get("title", "")
    url = item.get("url", "")
    ts = item.get("time_usec")

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
       domain = domain[4:]

    if not ts:
        continue

    combined_text = (title + " " + url).lower()

    # Er dette sandsynligvis fodbold?
    if not any(hint in combined_text for hint in FOOTBALL_HINTS):
        continue

    football_articles_found += 1
    source_scores[domain] += 1

    # Safari-tidsstempel i microseconds
    visited = datetime.fromtimestamp(
        ts / 1_000_000,
        tz=timezone.utc
    )

    age_days = max(
        (now - visited).days,
        0
    )

    # Recency-vægtning
    recency_weight = 1 / (1 + age_days / 30)

    words = re.findall(
        r"[a-zA-ZÆØÅæøå]{3,}",
        title.lower()
    )

    for word in words:

        if word in STOPWORDS:
            continue

        keywords[word] += recency_weight

        if word in TOPIC_WORDS:
            topics[word] += recency_weight

        if word in COMPETITIONS:
            competitions[word] += recency_weight

# ==================================================
# UDLED KLUBBER / INTERESSER
# ==================================================

for word, score in keywords.items():

    if score < 1:
        continue

    if word in STOPWORDS:
        continue

    if word in TOPIC_WORDS:
        continue

    if word in COMPETITIONS:
        continue

    teams[word] = score

# ==================================================
# OPBYG PROFIL
# ==================================================

print()
print("KILDER")

for domain, score in source_scores.items():
    print(domain, score)

profile = {
    "generated": datetime.now().isoformat(),
    "source_file": JSON_FILE,
    "football_articles_found": football_articles_found,

    "teams": dict(
        teams.most_common(25)
    ),

    "competitions": dict(
        competitions.most_common(15)
    ),

    "topics": dict(
        topics.most_common(15)
    ),

    "keywords": dict(
        keywords.most_common(50)
    )
}

sources = []

for domain, score in source_scores.items():

    source_type = discover_source_type(domain)

    sources.append({
        "name": domain,
        "type": source_type,
        "url": f"https://{domain}",
        "football_score": score
    })

sources.sort(
    key=lambda x: x["football_score"],
    reverse=True
)

# ==================================================
# GEM FIL
# ==================================================

with open(
    PROFILE_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        profile,
        f,
        ensure_ascii=False,
        indent=4
    )

with open(
    SOURCES_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        sources,
        f,
        ensure_ascii=False,
        indent=4
    )

print()
print("Sources gemt i:")
print(SOURCES_FILE)


# ==================================================
# RAPPORT
# ==================================================

print()
print("=" * 60)
print("FODBOLDPROFIL GENERERET")
print("=" * 60)
print()
print(f"Historiske fodboldartikler: {football_articles_found}")
print()
print("TOP 10 INTERESSER")
print()

for word, score in teams.most_common(10):
    print(f"{word:25} {score:.2f}")

print()
print("SOURCES")

for source in sources:

    print(
        source["name"],
        source["type"],
        source["football_score"]
    )
print("Profil gemt i:")
print(PROFILE_FILE)
print()