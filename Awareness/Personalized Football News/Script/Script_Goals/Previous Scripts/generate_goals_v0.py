# -*- coding: utf-8 -*-

import webbrowser
import csv
from collections import defaultdict

from select_goal_links import split_country_links

CSV_FILE = "Goals_Links.csv"
OUTPUT_FILE = "goals.html"


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


html = """
<div class="goals-box">

<table class="goals-table" style="border-spacing: 20px 10px;">
<tr>
    <th></th>
    <th align="left">Highlights</th>
    <th align="left">Goals</th>
</tr>
"""


for country in COUNTRIES:

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


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(html)

print(f"{OUTPUT_FILE} generated")