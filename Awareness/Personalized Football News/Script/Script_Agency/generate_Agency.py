
HTML_FILE = (
    BASE_DIR.parent.parent /
        "Website" /
        "IndexAgency.html"
)


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

html += """    
        </div>
    </div>        

    <div class="right-column">
        <h2>Produkt og hjemmeside under udvikling</h2>
        <p></p>
        <p></p>

        <div class="promo-section">
            <h2></h2>
            <p></p>
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
print(HTML_FILE)
print()