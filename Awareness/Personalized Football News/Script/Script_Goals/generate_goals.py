# ==================================================
# HTML
# ==================================================

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

"""


# -*- coding: utf-8 -*-

import webbrowser
import csv
from collections import defaultdict

from select_goal_links import split_country_links

CSV_FILE = "Goals_Links.csv"
OUTPUT_FILE = (
    BASE_DIR.parent.parent /
        "Website" /
        "IndexGoals.html"
)


COUNTRIES = [
    "Denmark",
    "England",
    "Spain",
    "Germany",
    "Italy",
    "France",
]


COUNTRY_IMAGES = {
    "Denmark": "Billeder/Denmark_Icon.jpg",
    "England": "Billeder/England_Icon.jpg",
    "Spain": "Billeder/Spain_Icon.jpg",
    "Germany": "Billeder/Germany_Icon.jpg",
    "Italy": "Billeder/Italy_Icon.jpg",
    "France": "Billeder/France_Icon.jpg"
}


def create_link(url, text):
    if not url or url == "NA":
        return "NA"
    else:
        return f'<a href="{url}" target="_blank">{text}</a>'
        


country_data = defaultdict(list)

with open(CSV_FILE, encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        country = row["Country"].strip()

        if country:
            country_data[country].append(row)


all_other_links = []


html += """
<div class="goals-box">

<table class="goals-table" style="border-spacing: 20px 10px;">
<tr>
    <th></th>
    <th align="left">Highlights</th>
    <th align="left">Goals</th>
</tr>
"""


for country in COUNTRIES:

    html += "<tr>"

    rows = country_data.get(country, [])

    (
        best_highlight,
        best_goal,
        other_links
    ) = split_country_links(rows)

    all_other_links.extend(other_links)

    image_file = COUNTRY_IMAGES.get(country, "")

    html += (
        f'<td>'
        f'<img src="{image_file}" height="40" '
        f'<img src="{image_file}" '
        f'</td>'
    )


    if best_highlight:
        html += (
       f"<td>{create_link(best_highlight['Link'], best_highlight['List1_Title'])}</td>"
    )
        
    else:
        html += "<td>NA</td>"

    if best_goal:
        html += (
       f"<td>{create_link(best_goal['Link'], best_goal['List1_Title'])}</td>"
    )
        
    else:
        html += "<td>NA</td>"

    html += "</tr>"


html += """

</table>

<hr>

<h3>Other Video Links</h3>

<ul>

"""


for row in all_other_links:

    link = row["Link"]

    if link == "NA":
        continue

    title = row["List2_Title"]

    html += (
        f"<li>{create_link(link, title)}</li>"
    )


html += """

</ul>

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
            <p>Præsentation af services og pakkeløsninger kommer her</p>
        </div>
    </div>

</div>

</body>
</html>
"""

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(html)

print(f"{OUTPUT_FILE} generated")