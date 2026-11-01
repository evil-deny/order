# 團購訂單系統

## 共用後台同步版本

原網址 <https://evil-deny.github.io/order/> 保留訂購、出貨與退貨介面，商品與訂單改由共用 API／資料庫管理。商品調價、庫存與隱藏狀態請到 <https://evil-deny.github.io/backstage/> 調整；顧客入口為 <https://evil-deny.github.io/customer/>。

員工開單與讀取訂單需要管理員登入。第一次從 order 進入時，按「前往管理員登入」，在 backstage 按「管理員登入」完成驗證後會返回 order。管理員權限由伺服器白名單驗證；舊版的瀏覽器密碼不再提供管理權限。登入連線保留於目前分頁，八小時到期，其他新分頁需要重新連接。

每 15 秒與切回頁面時同步資料。送單時先預留庫存，完成出貨時釋放未勾選品項的預留庫存；退貨與取消會由伺服器回補，所有入口共用同一份可售數量。自訂品項仍可開單，但只有管理員能建立自訂價格。

過季商品採隱藏，歷史訂單仍保留成交時的名稱與單價。原「刪除明細」改為取消待出貨訂單或封存已處理訂單，歷史資料留在後台。原本瀏覽器內的舊訂單／庫存資料未被刪除，也不會自動覆寫雲端資料；此版不提供自動歷史匯入。

`assets/cloud-sync.js` 與 backstage／customer 使用相同的公開 API。`work/build_order_page*.py` 是舊版靜態頁面產生器，不可直接用來覆寫此同步版本。商品日常維護請使用共用後台。

這是一個可直接部署到 GitHub Pages 的靜態網頁。

## 使用方式

- 網站入口：`index.html`
- 前台：訂購、出貨、退貨
- 後台：總覽、庫存

## GitHub Pages

建立 GitHub repo 後，將本專案推上去，再到 repo 的 Settings → Pages：

- Source 選 `Deploy from a branch`
- Branch 選 `main`
- Folder 選 `/root`

儲存後 GitHub 會產生公開網址。
