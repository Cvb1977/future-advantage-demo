import json
import re
from datetime import datetime, timezone
from collections import Counter

# ==================================================
# FILER
# ==================================================

JSON_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness"
    r"\Personalized Football News\Safari_Web_History\Historic.json"
)

PROFILE_FILE = (
    r"C:\Users\abc\OneDrive\Noah\Future Advantage\Awareness"
    r"\Script\Script_Profil\football_profile.json"
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

now = datetime.now(timezone.utc)

football_articles_found = 0

for item in history_items:

    title = item.get("title", "")
    url = item.get("url", "")
    ts = item.get("time_usec")

    if not ts:
        continue

    combined_text = (title + " " + url).lower()

    # Er dette sandsynligvis fodbold?
    if not any(hint in combined_text for hint in FOOTBALL_HINTS):
        continue

    football_articles_found += 1

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
print("Profil gemt i:")
print(PROFILE_FILE)
print()