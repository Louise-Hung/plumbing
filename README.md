# 公園導覽靜態網站

這個專案使用 `docs/` 目錄發布 GitHub Pages，將 CSV 中的公園資料轉成首頁與每座公園的獨立頁面。

## 重新產生網站
1. 安裝 Python 3（標準函式庫即可，無需額外套件）。
2. 在專案根目錄執行：
   ```bash
   python generate_sites.py
   ```
3. 產生的檔案會寫入 `docs/`（首頁）與 `docs/parks/`（個別公園頁面），直接推送即可更新 GitHub Pages。

來源資料位於 `從-google.com-抓取細節--2--2025-12-13.csv`，如需更新內容可先替換檔案再重新執行產生步驟。
