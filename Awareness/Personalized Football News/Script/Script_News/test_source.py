import requests
from bs4 import BeautifulSoup

url = "https://www.bold.dk"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("Status:", response.status_code)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

print()
print("LINKS FUNDET")
print("-" * 50)

count = 0

for a in soup.find_all("a", href=True):

    href = a["href"]
    text = a.get_text(strip=True)

    if len(text) > 10:

        print()
        print("Tekst:", text)
        print("Link :", href)

        count += 1

    if count >= 20:
        break