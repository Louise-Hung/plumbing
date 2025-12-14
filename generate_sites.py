from __future__ import annotations

import csv
import html
import pathlib
import re
import shutil
from typing import Iterable

ROOT = pathlib.Path(__file__).parent
DOCS_DIR = ROOT / "docs"
PARKS_DIR = DOCS_DIR / "parks"
DATA_FILE = ROOT / "從-google.com-抓取細節--2--2025-12-13.csv"


def slugify(value: str, seen: set[str]) -> str:
    value = value.strip()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^\w-]", "", value, flags=re.UNICODE)
    value = value.strip("-") or "park"
    value = value.lower()
    if value in seen:
        value = f"{value}-{len(seen)}"
    seen.add(value)
    return value


def load_parks() -> list[dict[str, str]]:
    parks: list[dict[str, str]] = []
    seen_slugs: set[str] = set()
    with DATA_FILE.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader, None)  # header row
        for row in reader:
            if not row or all(cell.strip() == "" for cell in row):
                continue
            map_url, image_url, name, rating, address, display_name, status = (cell.strip() for cell in row)
            status = " ".join(status.split())
            clean_status = "".join(ch for ch in status if ch.isprintable())
            title = display_name or name
            slug = slugify(title, seen_slugs)
            parks.append(
                {
                    "slug": slug,
                    "map_url": map_url,
                    "image_url": image_url,
                    "name": name or display_name,
                    "rating": rating,
                    "address": address,
                    "display_name": title,
                    "status": clean_status,
                }
            )
    return parks


def build_css() -> str:
    return (
        "body{font-family:Arial,Helvetica,sans-serif;margin:0;padding:0;background:#f3f4f6;color:#111827;}"
        "header,main,footer{max-width:1000px;margin:0 auto;padding:16px;}"
        "header{display:flex;justify-content:space-between;align-items:center;}"
        "a{color:#2563eb;text-decoration:none;}a:hover{text-decoration:underline;}"
        ".hero{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:center;}"
        ".hero img{width:100%;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.15);}"
        ".badge{display:inline-flex;align-items:center;gap:6px;background:#2563eb;color:white;padding:6px 10px;"
        "border-radius:999px;font-weight:bold;}"
        ".info{display:grid;gap:12px;margin-top:20px;}"
        "section{background:white;border-radius:12px;padding:16px;box-shadow:0 8px 20px rgba(0,0,0,0.08);}"
        "footer{margin:32px auto 40px;text-align:center;color:#6b7280;}"
        "@media(max-width:720px){.hero{grid-template-columns:1fr;}}"
        ".card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;}"
        ".card{background:white;border-radius:12px;box-shadow:0 6px 16px rgba(0,0,0,0.08);padding:12px;display:grid;gap:10px;}"
        ".card img{width:100%;height:160px;object-fit:cover;border-radius:10px;}"
        ".pill{background:#e5e7eb;border-radius:999px;padding:4px 10px;display:inline-block;font-size:12px;color:#374151;}"
    )


def render_index(parks: Iterable[dict[str, str]]) -> str:
    cards = []
    for park in parks:
        cards.append(
            f"<article class='card'>"
            f"<img src='{html.escape(park['image_url'])}' alt='{html.escape(park['display_name'])} 圖片'>"
            f"<h2><a href='parks/{html.escape(park['slug'])}/'>{html.escape(park['display_name'])}</a></h2>"
            f"<div class='pill'>⭐ {html.escape(park['rating'])}</div>"
            f"<p>{html.escape(park['address'])}</p>"
            f"<a href='{html.escape(park['map_url'])}'>在 Google Maps 查看</a>"
            f"</article>"
        )
    return f"""
<!doctype html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>公園導覽</title>
  <style>{build_css()}</style>
</head>
<body>
  <header>
    <div>
      <h1>公園導覽</h1>
      <p>從資料集中自動產生的 GitHub Pages 網站，每個公園都有自己的介紹頁面。</p>
    </div>
  </header>
  <main>
    <section>
      <div class="card-grid">
        {''.join(cards)}
      </div>
    </section>
  </main>
  <footer>資料來源：從 google.com 抓取的公園資訊</footer>
</body>
</html>
"""


def render_park(park: dict[str, str]) -> str:
    return f"""
<!doctype html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(park['display_name'])}</title>
  <style>{build_css()}</style>
</head>
<body>
  <header>
    <div>
      <a href="../../">← 返回公園導覽</a>
      <h1>{html.escape(park['display_name'])}</h1>
      <div class="badge">⭐ {html.escape(park['rating'])}</div>
    </div>
  </header>
  <main class="hero">
    <img src="{html.escape(park['image_url'])}" alt="{html.escape(park['display_name'])} 圖片">
    <section class="info">
      <div>
        <strong>地址：</strong>
        <p>{html.escape(park['address'])}</p>
      </div>
      <div>
        <strong>營業資訊：</strong>
        <p>{html.escape(park['status']) or '尚未提供營業資訊'}</p>
      </div>
      <div>
        <a class="badge" href="{html.escape(park['map_url'])}">在 Google Maps 打開</a>
      </div>
    </section>
  </main>
  <footer>透過資料檔自動產生的公園頁面</footer>
</body>
</html>
"""


def write_site(parks: list[dict[str, str]]) -> None:
    DOCS_DIR.mkdir(exist_ok=True)

    if PARKS_DIR.exists():
        shutil.rmtree(PARKS_DIR)
    PARKS_DIR.mkdir(parents=True, exist_ok=True)

    (DOCS_DIR / "index.html").write_text(render_index(parks), encoding="utf-8")

    for park in parks:
        park_dir = PARKS_DIR / park["slug"]
        park_dir.mkdir(parents=True, exist_ok=True)
        (park_dir / "index.html").write_text(render_park(park), encoding="utf-8")


def main() -> None:
    parks = load_parks()
    write_site(parks)


if __name__ == "__main__":
    main()
