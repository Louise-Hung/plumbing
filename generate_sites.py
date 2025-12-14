from __future__ import annotations
import csv
import html
import re
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path("google-2025-12-13.csv")
OUTPUT_DIR = Path("docs")
ASSETS_DIR = OUTPUT_DIR / "assets"
PARKS_DIR = OUTPUT_DIR / "parks"


class Park:
    def __init__(self, raw: Dict[str, str]):
        self.raw = raw
        self.name = raw.get("qBF1Pd", "").strip()
        self.slug = self._slugify(self.name)
        self.rating = raw.get("MW4etd", "").strip()
        self.review_count = raw.get("UY7F9", "").strip("() ")
        self.category = raw.get("W4Efsd", "").strip()
        self.category_note = raw.get("W4Efsd (7)", "").strip()
        self.address = raw.get("W4Efsd (4)", "").strip()
        self.hours = raw.get("W4Efsd (5)", "").strip()
        self.map_url = raw.get("hfpxzc href", "").strip()
        self.image_url = raw.get("FQ2IWe src", "").strip()
        self.review_snippet = self._combine_snippet([
            "ah5Ghc",
            "ah5Ghc (2)",
            "ah5Ghc (3)",
            "ah5Ghc (4)",
            "ah5Ghc (5)",
            "ah5Ghc (6)",
            "ah5Ghc (7)",
        ])
        self.highlights = [
            text
            for text in [
                raw.get("ah5Ghc (2)", "").strip(),
                raw.get("ah5Ghc (4)", "").strip(),
                raw.get("ah5Ghc (5)", "").strip(),
                raw.get("ah5Ghc (6)", "").strip(),
                raw.get("ah5Ghc (7)", "").strip(),
            ]
            if text
        ]

    @staticmethod
    def _slugify(name: str) -> str:
        base = re.sub(r"[^\w\u4e00-\u9fff]+", "-", name, flags=re.UNICODE).strip("-").lower()
        return base or "park"

    def _combine_snippet(self, keys: List[str]) -> str:
        parts = []
        for key in keys:
            value = self.raw.get(key, "") or ""
            cleaned = value.replace("\n", " ").strip().strip('"')
            if cleaned:
                parts.append(cleaned)
        return " ".join(parts)


def load_parks() -> List[Park]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_FILE}")

    with DATA_FILE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        parks: List[Park] = []
        existing_slugs: Dict[str, int] = {}
        for row in reader:
            name = (row.get("qBF1Pd") or "").strip()
            if not name:
                continue
            park = Park(row)
            # Ensure unique slug names
            count = existing_slugs.get(park.slug, 0)
            if count:
                park.slug = f"{park.slug}-{count+1}"
            existing_slugs[park.slug] = count + 1
            parks.append(park)
    return parks


def ensure_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    style = ASSETS_DIR / "style.css"
    style.write_text(
        """
:root {
  --bg: #f7f9fb;
  --card: #ffffff;
  --text: #1f2933;
  --muted: #52616b;
  --accent: #1c7ed6;
  --accent-dark: #1864ab;
  --shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
  font-family: 'Noto Sans TC', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
}

a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-dark); }

header.hero {
  padding: 48px 20px 32px;
  background: linear-gradient(135deg, #e9f3ff 0%, #f7f9fb 60%);
  text-align: center;
}

header.hero h1 {
  margin: 0 0 12px;
  font-size: 2.5rem;
}

header.hero p {
  margin: 0 auto;
  max-width: 720px;
  color: var(--muted);
  line-height: 1.6;
}

main { padding: 20px; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  max-width: 1200px;
  margin: 0 auto 48px;
}

.card {
  background: var(--card);
  border-radius: 14px;
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card img {
  width: 100%;
  height: 170px;
  object-fit: cover;
  background: #dce6f2;
}

.card .content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.meta { color: var(--muted); font-size: 0.95rem; }

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #e7f2ff;
  color: var(--accent-dark);
  font-weight: 600;
  font-size: 0.9rem;
}

.park-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
}

.park-hero img {
  width: 100%;
  max-height: 360px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: var(--shadow);
}

.detail-list {
  list-style: none;
  padding: 0;
  margin: 12px 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 8px 16px;
}

.detail-list li { color: var(--muted); }

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}

.tag {
  background: #eef2f7;
  color: var(--text);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 0.9rem;
}

blockquote {
  margin: 12px 0;
  padding: 16px;
  background: #eef5ff;
  border-radius: 10px;
  color: #233143;
  line-height: 1.5;
}

.footer {
  text-align: center;
  padding: 24px 0;
  color: var(--muted);
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  background: var(--accent);
  color: white;
  font-weight: 600;
  box-shadow: var(--shadow);
  width: fit-content;
}

.button:hover {
  background: var(--accent-dark);
}
""",
        encoding="utf-8",
    )


def render_index(parks: List[Park]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = []
    for park in parks:
        image = html.escape(park.image_url or "https://via.placeholder.com/400x200?text=Park")
        card = f"""
        <article class=\"card\">
          <img src=\"{image}\" alt=\"{html.escape(park.name)}\">
          <div class=\"content\">
            <div class=\"badge\">⭐ {html.escape(park.rating or 'N/A')} · {html.escape(park.review_count or '0')} 則評價</div>
            <h2><a href=\"parks/{park.slug}/index.html\">{html.escape(park.name)}</a></h2>
            <div class=\"meta\">{html.escape(park.address or '地址未提供')}</div>
            <div class=\"meta\">{html.escape(park.category or '公園')}</div>
          </div>
        </article>
        """
        cards.append(card)

    index_html = f"""
<!doctype html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>公園地圖 | GitHub Pages</title>
  <link rel=\"stylesheet\" href=\"assets/style.css\">
</head>
<body>
  <header class=\"hero\">
    <h1>公園地圖</h1>
    <p>自動從資料集中生成的公園索引。點擊卡片即可前往每一個公園的獨立介紹頁，適合部署到 GitHub Pages。</p>
  </header>
  <main>
    <section class=\"grid\">
      {''.join(cards)}
    </section>
  </main>
  <div class=\"footer\">由 google-2025-12-13.csv 自動產生</div>
</body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")


def render_park_page(park: Park):
    park_dir = PARKS_DIR / park.slug
    park_dir.mkdir(parents=True, exist_ok=True)
    image = html.escape(park.image_url or "https://via.placeholder.com/900x400?text=Park")
    tags = [t for t in [park.category, park.category_note] if t]
    tags.extend(park.highlights)
    tag_html = "".join(f"<span class=\"tag\">{html.escape(tag)}</span>" for tag in tags)
    snippet_html = f"<blockquote>{html.escape(park.review_snippet)}</blockquote>" if park.review_snippet else ""

    content = f"""
<!doctype html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{html.escape(park.name)} | 公園地圖</title>
  <link rel=\"stylesheet\" href=\"../../assets/style.css\">
</head>
<body>
  <main class=\"park-page\">
    <p><a href=\"../../index.html\">← 返回索引</a></p>
    <h1>{html.escape(park.name)}</h1>
    <div class=\"badge\">⭐ {html.escape(park.rating or 'N/A')} · {html.escape(park.review_count or '0')} 則評價</div>
    <div class=\"park-hero\">
      <img src=\"{image}\" alt=\"{html.escape(park.name)}\">
    </div>
    <ul class=\"detail-list\">
      <li><strong>地址：</strong> {html.escape(park.address or '未提供')}</li>
      <li><strong>營業資訊：</strong> {html.escape(park.hours or '未提供')}</li>
      <li><strong>分類：</strong> {html.escape(park.category or '公園')}</li>
    </ul>
    <div class=\"tag-row\">{tag_html}</div>
    {snippet_html}
    <p><a class=\"button\" href=\"{html.escape(park.map_url)}\" target=\"_blank\" rel=\"noopener noreferrer\">在 Google Maps 開啟</a></p>
  </main>
</body>
</html>
"""
    (park_dir / "index.html").write_text(content, encoding="utf-8")


def main():
    parks = load_parks()
    ensure_assets()
    render_index(parks)
    for park in parks:
        render_park_page(park)


if __name__ == "__main__":
    main()
