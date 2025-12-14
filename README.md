# 公園資料 GitHub Pages 生成器

這個專案包含從 Google 搜尋結果匯出的公園資料（CSV），並提供一支 `generate_sites.py` 腳本，把每一筆公園資料轉成 GitHub Pages 可用的靜態網站：

- `docs/index.html`：公園清單首頁，卡片式連結到各公園頁面。
- `docs/parks/<slug>/index.html`：每個公園的獨立頁面，包含名稱、評分、地址、營業資訊、照片與前往 Google Maps 的連結。

## 如何產生網站
1. 確保資料檔 `從-google.com-抓取細節--2--2025-12-13.csv` 位於專案根目錄。
2. 執行腳本：
   ```bash
   python generate_sites.py
   ```
3. 生成結果會寫入 `docs/`，可直接部署為 GitHub Pages（設定 Pages 來源為 `docs/` 資料夾）。

## GitHub Pages 設定建議
1. 在 GitHub 專案的 **Settings → Pages**，將 **Source** 選擇為 **Deploy from a branch**，資料夾選擇 `docs/`。
2. 儲存後，GitHub Pages 即會發佈 `docs/` 的內容；首頁為 `index.html`，各公園位於 `/parks/<slug>/`。

若重新匯入新的資料檔，重跑腳本即可重新產生整份網站。腳本會自動清理舊的 `docs/parks/` 內容並重建，確保資料一致。
