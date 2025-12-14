# 公園 GitHub Pages 網站

利用資料集自動為每座公園產生靜態網站，放在 `docs/` 目錄供 GitHub Pages 使用。所有頁面皆由 `generate_sites.py` 根據 `從-google.com-抓取細節--2--2025-12-13.csv` 生成，並將結構化資料輸出為 `data/parks.json` 供參考。

## 主要內容
- `docs/index.html`：公園總覽卡片，連結到各公園的獨立頁面。
- `docs/parks/<公園名稱>.html`：每個公園的介紹頁面，包含評分、地址、營業資訊與 Google 地圖連結。
- `docs/styles.css`：簡單的排版樣式，讓卡片與詳細頁面易讀。
- `data/parks.json`：整理後的公園資料，可重複利用。

## 更新流程
1. 確保系統有 Python 3。
2. 在專案根目錄執行：
   ```bash
   python generate_sites.py
   ```
   指令會重新整理 `data/` 與 `docs/parks/` 內容。
3. 將變更推送到 GitHub，並在 GitHub Pages 設定中選擇 `main` 分支的 `docs/` 作為站點來源。

## 資料來源
- `從-google.com-抓取細節--2--2025-12-13.csv`：原始公園清單與資訊。
- `google-2025-12-13.csv`：原始抓取資料，保留以供參考。
