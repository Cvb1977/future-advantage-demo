from Get_HTML_Articles_Function import get_html_articles

articles = get_html_articles(
    "Bold",
    "https://www.bold.dk"
)

print()
print("Antal artikler:", len(articles))
print()

for article in articles[:20]:

    print(article["title"])
    print(article["url"])
    print("-" * 80)