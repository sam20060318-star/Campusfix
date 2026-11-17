# CampusFix

一個讓學生回報校園問題並追蹤處理進度的小型網頁應用程式。
學生可以提交與搜尋回報；Staff 可以檢視回報、記錄處理進度，並填寫備註後結案。

使用 **HTML/CSS/JavaScript + Python Flask + SQLite**。在本機執行，所有資料皆為虛構。

## 1. 安裝與啟動

需求：Python 3.10 以上。Node.js 18 以上只有執行前端測試時才需要。

**Windows（PowerShell）**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py --seed-demo
```

如果第二行出現「已停用指令碼執行」的錯誤，先執行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 再重試。

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py --seed-demo
```

接著用瀏覽器打開 <http://127.0.0.1:5000/>。在終端機按 `Ctrl+C` 可停止。

- `--seed-demo` **只有在資料庫是空的時候**才會加入三筆虛構回報，不會刪除任何資料。不加這個參數就會以目前已保存的資料啟動。
- 如果 5000 埠被占用，可用 `--port 5001` 更換。
- 想從空的資料庫重新開始，先停止應用程式，再刪除 `instance` 資料夾。

## 2. 示範帳號

以下是為了展示自動建立的虛構帳號，請勿使用真實密碼。

| 角色 | 帳號 | 密碼 | 可以做什麼 |
| --- | --- | --- | --- |
| Staff | `staff` | `staff123` | 開啟管理頁、變更狀態、填寫備註後結案 |
| 學生 | `student` | `student123` | 可以登入，但開啟管理頁與呼叫更新 API 都會被拒絕（HTTP 403） |

學生頁面不需要登入。Staff 管理頁在 <http://127.0.0.1:5000/staff>（上方導覽列的「Staff 管理」連結）。

## 3. 頁面

| 網址 | 用途 | Story |
| --- | --- | --- |
| `/` | 學生頁：提交回報、列表、詳情、關鍵字搜尋、地點篩選 | S1、S2、S3、S7、S8 |
| `/login` | 用示範帳號登入 | S9 |
| `/staff` | Staff 管理頁：回報列表、打開單筆、變更狀態、填寫備註後結案 | S4、S5、S6 |

## 4. 搜尋與篩選的行為

- **關鍵字**：出現在標題**或**描述中就算符合，不分英文大小寫（`wi-fi`、`WI-FI`、`Wi-Fi` 的結果相同）。
- **地點**：必須與已保存的地點名稱整個相同，不分英文大小寫（`圖書館` 符合 `圖書館`，`library` 符合 `Library`；只打 `圖書` 不符合）。地點輸入框會提示已存在的地點。
- **關鍵字與地點同時指定時採 AND**：回報必須兩者都符合才會顯示。
- 空白的條件會被忽略。按「清除條件」會回到完整列表。

## 5. 介面語言與狀態名稱

- 網站介面與提示訊息為繁體中文。
- 狀態在資料庫與 API 中保存為作業規定的英文值 `Submitted`、`In Progress`、`Resolved`，畫面上以「已提交 Submitted」、「處理中 In Progress」、「已解決 Resolved」顯示。

## 6. 資料與持久化

- 回報、狀態與處理備註存放在 SQLite 檔案 `instance/campusfix.db`，重新整理頁面與重新啟動應用程式後都還在。
- 設定環境變數 `CAMPUSFIX_DB` 可改用其他資料庫檔案。
- 回報 ID 由資料庫產生（`AUTOINCREMENT`），不會重複使用。
- `instance/` 已排除在 Git 之外，所以每台電腦有各自的本機資料。

## 7. API

| 方法與路徑 | 行為 |
| --- | --- |
| `POST /api/reports` | 傳入 JSON，含 `title`、`location`、`category`、`description`（全部必填，不可空白）。成功回傳 `201` 與已保存的回報，內含唯一的 `id` 與 `status: "Submitted"`。輸入無效時回傳 `400` 與 `{"error": "請輸入地點。", "errors": {...}}`，不會保存任何資料。 |
| `GET /api/reports?keyword=&location=` | 回傳 JSON 陣列，新的在前。篩選規則見第 4 節。 |
| `GET /api/reports/<id>` | 回傳單筆回報；不存在時回傳 `404` 與 `{"error": "找不到這筆報修。"}`。 |
| `GET /api/locations` | 已保存的地點名稱，用於輸入提示。 |
| `POST /api/login` | 傳入 JSON `username`、`password`。錯誤時回傳 `401`。 |
| `POST /api/logout`、`GET /api/me` | 結束登入狀態；查詢目前登入者。 |
| `PATCH /api/reports/<id>/status` | **僅限 Staff。** 傳入 JSON `status`（`Submitted`、`In Progress`、`Resolved`），設為 `Resolved` 時還需要非空白的 `resolution_note`。未登入 → `401`；學生 → `403`；狀態無效或缺少備註 → `400`。所有被拒絕的情況下，已保存的資料都不會改變。 |

角色是由伺服器依登入帳號判定的。保護更新動作的是伺服器端的檢查，不是在瀏覽器隱藏按鈕。

回報的 JSON 格式：

```json
{"id": 4, "title": "投影機無法開機", "location": "教室 A101", "category": "教室設備",
 "description": "按下電源鍵後投影機沒有反應。", "status": "Submitted", "resolution_note": "",
 "created_at": "2026-11-15 14:00:00", "updated_at": "2026-11-15 14:00:00"}
```

## 8. 測試

```bash
python -m pytest -v
node --test tests/student.test.mjs
```

- `tests/test_api.py`：對真實的 Flask 應用程式與暫時的 SQLite 檔案做測試。測試名稱帶有 `docs/TEST_RECORD.md` 使用的測試 ID（TC01–TC13）。
- `tests/test_restart.py`：啟動真實的伺服器行程、停止、再啟動，確認回報、狀態與備註都還在。
- `tests/student.test.mjs`：學生頁與 Staff 頁在瀏覽器端的驗證與請求組合。
- `tests/e2e_staff_race.cjs`（選用）：用真的瀏覽器重現「Staff 快速切換報修時，較慢的回應把畫面切回前一筆」的缺陷，確認已修正。需要先執行 `npm install --no-save playwright` 與 `npx playwright install chromium`，再執行 `node tests/e2e_staff_race.cjs`。

## 9. 專案結構

```text
app.py                  Flask 應用程式：頁面、API、登入與 Staff 授權
db.py                   SQLite 資料表與查詢
templates/index.html    學生頁
templates/login.html    登入頁
templates/staff.html    Staff 管理頁
static/css/             student.css、staff.css
static/js/              student.js、login.js、staff.js
tests/                  test_api.py、test_restart.py、student.test.mjs
docs/                   Jira 清單、教授要求對照表、測試紀錄
```

## 10. 已知限制

- 只供本機展示；Flask 開發伺服器不適合公開部署。
- 只有兩個固定的示範帳號，沒有註冊或修改密碼功能。
- 任何人不需登入就能提交與查看回報，只有 Staff 的更新動作受到限制。
- 回報提交後無法編輯或刪除。
- 把已結案的回報改回其他狀態時，處理備註會被清空。

## 11. 團隊報告

團隊分工、實作證據、測試成果及開發工具使用說明收錄於課程團隊報告。
