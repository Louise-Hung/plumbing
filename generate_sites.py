import csv
import html
import re
from pathlib import Path
from urllib.parse import quote

SOURCE = Path("從-google.com-抓取細節--2--2025-12-13.csv")
DOCS_DIR = Path("docs")
PARKS_DIR = DOCS_DIR / "parks"


def slugify(name: str, existing: set[str]) -> str:
    base = re.sub(r"\s+", "-", name.strip())
    base = re.sub(r"[^\w\-\u4e00-\u9fff]", "", base)
    base = base.strip("-") or "park"
    slug = base
    counter = 2
    while slug in existing:
        slug = f"{base}-{counter}"
        counter += 1
    existing.add(slug)
    return slug


def load_parks():
    with SOURCE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        parks = []
        for row in reader:
            name = row["DUwDvf"].strip()
            if not name:
                continue
            parks.append(
                {
                    "name": name,
                    "map_url": row["hfpxzc href"].strip(),
                    "image_url": row["aoRNLd src"].strip(),
                    "rating": row["F7nice"].strip(),
                    "address": row["Io6YTe"].strip(),
                    "alias": row["DkEaL"].strip(),
                    "hours": row["o0Svhf"].strip().replace("\ue5cf", "").replace("\n", " ").strip(),
                }
            )
    return parks


def build_index(parks):
    cards = []
    for park in parks:
        cards.append(
            f"""
            <article class=\"card\">
                <img src=\"{html.escape(park['image_url'])}\" alt=\"{html.escape(park['name'])}\" loading=\"lazy\" />
                <h2>{html.escape(park['name'])}</h2>
                <p class=\"meta\">評分：{html.escape(park['rating'])}</p>
                <p>{html.escape(park['address'])}</p>
                <a class=\"button\" href=\"parks/{quote(park['slug'])}.html\">查看公園介紹</a>
            </article>
            """
        )

    cards_html = "".join(cards)
    return """
<!doctype html>
<html lang=\"zh-TW\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>公園導覽</title>
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
    <link href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600&display=swap\" rel=\"stylesheet\">
    <style>
        :root {{ color-scheme: light; }}
        body {{ font-family: 'Noto Sans TC', sans-serif; margin: 0; background: #f7f7f7; color: #222; }}
        header {{ padding: 2rem 1.5rem 1rem; text-align: center; background: linear-gradient(135deg, #8BC6EC 0%, #9599E2 100%); color: #fff; }}
        main {{ max-width: 1200px; margin: 0 auto; padding: 1.5rem; }}
        .grid {{ display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
        .card {{ background: #fff; border-radius: 12px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); padding: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }}
        .card img {{ width: 100%; height: 180px; object-fit: cover; border-radius: 10px; }}
        .card h2 {{ margin: 0.25rem 0 0; font-size: 1.2rem; }}
        .meta {{ color: #6b7280; margin: 0; }}
        .card p {{ margin: 0; line-height: 1.5; }}
        .button {{ margin-top: auto; display: inline-block; text-decoration: none; color: #fff; background: #2563eb; padding: 0.6rem 0.9rem; border-radius: 8px; text-align: center; font-weight: 600; }}
        .button:hover {{ background: #1d4ed8; }}
    </style>
</head>
<body>
    <header>
        <h1>公園導覽</h1>
        <p>瀏覽每一座公園的簡介、位置與營業資訊。</p>
    </header>
    <main>
        <section class=\"grid\">
            {cards}
        </section>
    </main>
</body>
</html>
""".format(cards=cards_html)


def build_park_page(park):
    return """
<!doctype html>
<html lang=\"zh-TW\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{name} | 公園導覽</title>
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
    <link href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600&display=swap\" rel=\"stylesheet\">
    <style>
        body {{ font-family: 'Noto Sans TC', sans-serif; margin: 0; background: #f8fafc; color: #111827; }}
        header {{ padding: 1rem 1.5rem; background: #fff; box-shadow: 0 3px 12px rgba(0,0,0,0.08); position: sticky; top: 0; }}
        main {{ max-width: 900px; margin: 0 auto; padding: 1.5rem; }}
        .hero {{ width: 100%; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.12); }}
        h1 {{ margin: 1rem 0 0.25rem; font-size: 2rem; }}
        .pill {{ display: inline-flex; gap: 0.4rem; align-items: center; background: #e0f2fe; color: #075985; padding: 0.35rem 0.7rem; border-radius: 999px; font-weight: 600; }}
        .info {{ margin: 1rem 0; padding: 1rem; background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
        .info p {{ margin: 0.3rem 0; line-height: 1.6; }}
        .actions {{ display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap; }}
        a.button {{ text-decoration: none; color: #fff; background: #2563eb; padding: 0.65rem 1rem; border-radius: 10px; font-weight: 700; }}
        a.secondary {{ background: #10b981; }}
        a:hover {{ filter: brightness(0.95); }}
    </style>
</head>
<body>
    <header>
        <a href=\"../index.html\" aria-label=\"返回列表\">← 返回公園列表</a>
    </header>
    <main>
        <img class=\"hero\" src=\"{image}\" alt=\"{name}\" loading=\"lazy\" />
        <h1>{name}</h1>
        <div class=\"pill\">⭐ 評分 {rating}</div>
        <section class=\"info\">
            <p><strong>地址：</strong>{address}</p>
            <p><strong>營業資訊：</strong>{hours}</p>
            <p><strong>別名：</strong>{alias}</p>
        </section>
        <div class=\"actions\">
            <a class=\"button\" href=\"{map_url}\" target=\"_blank\" rel=\"noopener\">在地圖上開啟</a>
            <a class=\"button secondary\" href=\"../index.html\">回到首頁</a>
        </div>
    </main>
</body>
</html>
""".format(
        name=html.escape(park["name"]),
        rating=html.escape(park["rating"]),
        address=html.escape(park["address"]),
        hours=html.escape(park["hours"] or "—"),
        alias=html.escape(park["alias"] or park["name"]),
        map_url=html.escape(park["map_url"]),
        image=html.escape(park["image_url"]),
    )


def main():
    parks = load_parks()
    DOCS_DIR.mkdir(exist_ok=True)
    PARKS_DIR.mkdir(parents=True, exist_ok=True)

    slugs: set[str] = set()
    for park in parks:
        park["slug"] = slugify(park["name"], slugs)

    index_html = build_index(parks)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for park in parks:
        page_html = build_park_page(park)
        (PARKS_DIR / f"{park['slug']}.html").write_text(page_html, encoding="utf-8")


if __name__ == "__main__":
    main()
