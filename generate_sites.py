import csv
import json
import pathlib
import re
import shutil
from typing import List, Dict

ROOT = pathlib.Path(__file__).parent
CSV_PATH = ROOT / "從-google.com-抓取細節--2--2025-12-13.csv"
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
PARKS_DIR = DOCS_DIR / "parks"


def slugify(text: str) -> str:
    base = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", text).strip("-")
    return base or "park"


def load_parks() -> List[Dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        parks = []
        for idx, row in enumerate(reader, start=1):
            name = (row.get("DUwDvf") or "").strip()
            fallback_name = (row.get("DkEaL") or "").strip()
            rating = (row.get("F7nice") or "").strip()
            address = (row.get("Io6YTe") or "").strip()
            hours = (row.get("o0Svhf") or "").replace("\\n", " ").strip()
            map_url = (row.get("hfpxzc href") or "").strip()
            image_url = (row.get("aoRNLd src") or "").strip()

            if not any([name, fallback_name, map_url, image_url]):
                continue

            display_name = name or fallback_name or f"公園 {idx}"
            parks.append(
                {
                    "slug": slugify(display_name) or f"park-{idx}",
                    "name": display_name,
                    "rating": rating,
                    "address": address,
                    "hours": hours,
                    "map_url": map_url,
                    "image_url": image_url,
                }
            )
    return parks


def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    if PARKS_DIR.exists():
        shutil.rmtree(PARKS_DIR)
    DOCS_DIR.mkdir(exist_ok=True)
    PARKS_DIR.mkdir(parents=True, exist_ok=True)


def write_json(parks: List[Dict[str, str]]):
    output = DATA_DIR / "parks.json"
    output.write_text(json.dumps(parks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


def build_index(parks: List[Dict[str, str]]):
    cards = []
    for park in parks:
        cards.append(
            f"""
        <article class=\"card\">
          <img src=\"{park['image_url']}\" alt=\"{park['name']}\" loading=\"lazy\" />
          <div class=\"card-body\">
            <h2>{park['name']}</h2>
            <p class=\"meta\">評分：{park['rating'] or '未提供'}</p>
            <p class=\"meta\">地址：{park['address'] or '未提供'}</p>
            <p class=\"meta\">營業資訊：{park['hours'] or '未提供'}</p>
            <div class=\"links\">
              <a class=\"btn\" href=\"parks/{park['slug']}.html\">查看公園頁面</a>
              <a class=\"btn secondary\" href=\"{park['map_url']}\" target=\"_blank\" rel=\"noopener noreferrer\">在地圖開啟</a>
            </div>
          </div>
        </article>
        """
        )

    content = f"""<!doctype html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>公園目錄 | GitHub Pages</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <header class=\"page-header\">
    <h1>公園目錄</h1>
    <p>從資料集中為每座公園建立的 GitHub Pages 站點。</p>
  </header>
  <main class=\"grid\">
    {''.join(cards)}
  </main>
</body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(content, encoding="utf-8")
    print(f"Wrote docs/index.html")


def build_detail_page(park: Dict[str, str]):
    content = f"""<!doctype html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{park['name']} | 公園介紹</title>
  <link rel=\"stylesheet\" href=\"../styles.css\" />
</head>
<body>
  <header class=\"page-header\">
    <p><a href=\"../index.html\">← 返回公園目錄</a></p>
    <h1>{park['name']}</h1>
  </header>
  <main class=\"detail\">
    <img class=\"hero\" src=\"{park['image_url']}\" alt=\"{park['name']}\" />
    <section class=\"info\">
      <p><strong>評分：</strong>{park['rating'] or '未提供'}</p>
      <p><strong>地址：</strong>{park['address'] or '未提供'}</p>
      <p><strong>營業資訊：</strong>{park['hours'] or '未提供'}</p>
      <p><a class=\"btn\" href=\"{park['map_url']}\" target=\"_blank\" rel=\"noopener noreferrer\">在 Google 地圖查看</a></p>
    </section>
  </main>
</body>
</html>
"""
    path = PARKS_DIR / f"{park['slug']}.html"
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def build_detail_pages(parks: List[Dict[str, str]]):
    for park in parks:
        build_detail_page(park)


def main():
    ensure_dirs()
    parks = load_parks()
    write_json(parks)
    build_index(parks)
    build_detail_pages(parks)


if __name__ == "__main__":
    main()
