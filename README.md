# 公園 GitHub Pages 產生器

此專案將 `google-2025-12-13.csv` 裡的公園資料自動轉成 GitHub Pages 靜態網站：

- `docs/index.html`：公園清單與連結卡片。
- `docs/parks/<slug>/index.html`：每個公園各自的獨立介紹頁（地址、營業資訊、特色標籤、評論摘要與 Google Maps 連結）。
- `docs/assets/style.css`：統一的網頁樣式。

## 如何重新產生頁面

1. 確保 `google-2025-12-13.csv` 在專案根目錄。
2. 執行產生腳本：
   ```bash
   python generate_sites.py
   ```
   執行後 `docs/` 會被重新建立，並生成所有公園的獨立頁面。

## GitHub Pages 設定

1. 將 Repository 的 GitHub Pages 來源設定為 **`/docs`** 資料夾。
2. 推送後即可在 Pages 網址下瀏覽公園索引與每個公園的介紹頁。
