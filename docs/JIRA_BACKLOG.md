# CampusFix｜Jira 專案 Backlog 與執行紀錄

**專案：** SE_CampusFix_Team05（Jira Key：`CM`）  
**整理日期：** 2026-11-19  
**範圍：** 3 個 Epic、9 張 Story、35 張 Subtask、10 張 Task、1 張 Bug。  
**進度：** 9 張 Story 及 35 張 Subtask 均已完成；兩個正式 Sprint 已關閉。專案共 58 個工作項目，其中 52 項完成、6 項待辦（CM-49、CM-50、CM-51、CM-53、CM-56、CM-58）。

## 角色與分工

| 成員 | Scrum 角色 | 主要負責範圍 |
| --- | --- | --- |
| 陳萬祥 | Product Owner（PO） | Backlog 需求與排序、學生端頁面、列表及地點篩選 |
| 龔國煌 | Scrum Master（SM） | Sprint 協調、報修 API、資料保存、關鍵字搜尋 |
| 張廷碩 | Developer | Staff 管理、登入權限、狀態更新及結案 |
| 劉智丞 | Developer | 整合、測試執行與缺陷複測 |

工作項目的 Jira 狀態以 CM 看板為準；技術實作與驗收細節以下列項目及 `docs/TEST_RECORD.md` 為依據。任務的補充紀錄與正式審查、實際會議或影片完成狀態分別記載。

## 階層總覽

```text
Epic 1 問題回報（CM-2）                         已完成
  └─ S1 提交問題回報（CM-5）                    5 點｜Sprint 1｜完成
Epic 2 報修追蹤與搜尋（CM-3）                   已完成
  ├─ S2 查看報修列表（CM-6）                    2 點｜Sprint 1｜完成
  ├─ S3 查看詳情與狀態（CM-7）                  2 點｜Sprint 1｜完成
  ├─ S7 關鍵字搜尋（CM-11）                     3 點｜Sprint 2｜完成
  └─ S8 依地點篩選（CM-12）                     2 點｜Sprint 2｜完成
Epic 3 Staff 處理管理（CM-4）                  已完成
  ├─ S9 Staff 權限控管（CM-13）                 5 點｜Sprint 2｜完成
  ├─ S4 Staff 查看報修（CM-8）                  2 點｜Sprint 2｜完成
  ├─ S5 更新報修狀態（CM-9）                    2 點｜Sprint 2｜完成
  └─ S6 填寫備註後結案（CM-10）                 5 點｜Sprint 2｜完成
Task：T1～T10（CM-49～CM-58）
Bug：Staff 快速切換案件，可能更新錯誤報修（CM-59） 已完成
```

Sprint 1：3 張 Story，9 點；Sprint 2：6 張 Story，19 點。合計 **28 Story Points**。

---

## Epic 1｜Problem Reporting（問題回報）

**說明**　學生可以填寫必要資訊回報校園問題，系統會驗證內容並永久保存。

### S1　Submit a Problem Report（提交問題回報）　`CM-5`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要提交校園問題回報，以便 Staff 能夠調查處理。 |
| 優先級 | High。其他所有功能都依賴已保存的回報。 |
| Story Points | 5（Jira 現有估點） |
| Sprint | 1 |
| Jira 狀態 | 完成 |
| 負責人 | 龔國煌（後端）＋陳萬祥（表單） |
| 相依 | 無 |
| 程式位置 | `app.py` → `validate_report`、`create_report`；`db.py` → `SCHEMA`、`create_report`；`templates/index.html`；`static/js/student.js` → `validateReport`、`createReport` |
| 測試位置 | `tests/test_api.py` → `test_tc01…`、`test_tc02…`、`test_tc03…`、`test_tc04…`；`tests/test_restart.py`；`tests/student.test.mjs` |

**驗收條件**

1. 有效的提交會保存四個必填欄位（標題、地點、分類、描述）。
2. 缺少必填欄位或只填空白時無法提交，畫面在該欄位顯示明確訊息。直接對 API 送出同樣的請求也會被拒絕，資料庫不會新增資料。
3. 提交成功後顯示唯一的回報 ID 與狀態 `Submitted`。分別提交兩筆會得到不同的 ID。
4. 重新整理頁面及重新啟動應用程式後，已保存的回報仍然查得到。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-14](https://sidspaces.atlassian.net/browse/CM-14) | 建立 `reports` 資料表與 SQLite 儲存，ID 由資料庫產生 | 實作 | 龔國煌 |
| [CM-15](https://sidspaces.atlassian.net/browse/CM-15) | 實作 `POST /api/reports`，在伺服器端驗證四個欄位 | 實作 | 龔國煌 |
| [CM-16](https://sidspaces.atlassian.net/browse/CM-16) | 學生表單串接 API，顯示欄位錯誤、新 ID 與狀態 | 實作 | 陳萬祥 |
| [CM-17](https://sidspaces.atlassian.net/browse/CM-17) | 測試有效提交、空白欄位（畫面與直接打 API）、唯一 ID | 測試 | 劉智丞 |
| [CM-18](https://sidspaces.atlassian.net/browse/CM-18) | 測試重新整理與重啟後資料仍在 | 測試 | 劉智丞 |

---

## Epic 2｜Report Tracking and Search（回報追蹤與搜尋）

**說明**　學生可以瀏覽已保存的回報、打開單筆查看詳情與目前狀態，並在新增回報前先搜尋或篩選。

### S2　View Report List（查看回報列表）　`CM-6`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要看到已保存的回報，以便找到某個問題和它的狀態。 |
| 優先級 | High。這是追蹤回報的入口。 |
| Story Points | 2（Jira 現有估點） |
| Sprint | 1 |
| Jira 狀態 | 完成 |
| 負責人 | 陳萬祥（主責），龔國煌提供 API |
| 相依 | S1 |
| 程式位置 | `app.py` → `list_reports`；`db.py` → `list_reports`；`static/js/student.js` → `loadReports`、`renderReport` |
| 測試位置 | `tests/test_api.py` → `test_list_is_empty_before_any_report`、`test_tc05…` |

**驗收條件**

1. 列表顯示資料庫中已保存的回報。
2. 每一筆至少顯示回報 ID、標題和目前狀態。
3. 新提交的回報不需重啟應用程式就會出現在列表中。
4. 沒有任何回報時，畫面顯示空狀態訊息，不是一片空白。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-19](https://sidspaces.atlassian.net/browse/CM-19) | 實作 `GET /api/reports`，回傳已保存的回報，新的在前 | 實作 | 龔國煌 |
| [CM-20](https://sidspaces.atlassian.net/browse/CM-20) | 顯示列表（ID、標題、狀態），以及空狀態與錯誤狀態 | 實作 | 陳萬祥 |
| [CM-21](https://sidspaces.atlassian.net/browse/CM-21) | 測試列表與已保存資料一致，包含空列表 | 測試 | 劉智丞 |

### S3　View Report Details and Status（查看回報詳情與狀態）　`CM-7`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要查看單筆回報的詳情與目前狀態，以便追蹤處理進度。 |
| 優先級 | High。學生需要它才能追蹤個別回報。 |
| Story Points | 2（Jira 現有估點） |
| Sprint | 1；Sprint 2 延伸驗證更新狀態 |
| Jira 狀態 | 完成 |
| 負責人 | 陳萬祥（主責），龔國煌提供單筆 API |
| 相依 | S2 |
| 程式位置 | `app.py` → `get_report`；`db.py` → `get_report`；`static/js/student.js` → `showDetails` |
| 測試位置 | `tests/test_api.py` → `test_tc05…`、`test_tc13_unknown_report_id_returns_404` |

**驗收條件**

1. 在列表選取一筆回報，會開啟相同 ID 的詳情，顯示標題、地點、分類、描述和狀態。
2. 重新開啟詳情時會讀取最新保存的狀態。已結案的回報同時顯示處理備註。
3. 不存在的 ID 回傳 HTTP 404，畫面顯示友善的錯誤訊息。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-22](https://sidspaces.atlassian.net/browse/CM-22) | 實作 `GET /api/reports/<id>`，找不到時回傳 404 | 實作 | 龔國煌 |
| [CM-23](https://sidspaces.atlassian.net/browse/CM-23) | 串接詳情視窗，包含處理備註與錯誤訊息 | 實作 | 陳萬祥 |
| [CM-24](https://sidspaces.atlassian.net/browse/CM-24) | 測試詳情與列表一致、404 情況、Staff 更新後的狀態 | 測試 | 劉智丞 |

### S7　Search Reports by Keyword（關鍵字搜尋回報）　`CM-11`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要搜尋回報的標題與描述，以便在提交新回報前確認是否已有人回報。 |
| 優先級 | High。Sprint 2 新增搜尋需求，可減少重複回報。 |
| Story Points | 3（Jira 現有估點） |
| Sprint | 2 |
| Jira 狀態 | 完成 |
| 負責人 | 龔國煌（搜尋）＋陳萬祥（畫面） |
| 相依 | S2 |
| 程式位置 | `db.py` → `list_reports`（`CASEFOLD` + `instr`）；`static/js/student.js` → `buildReportUrl`、`loadReports` |
| 測試位置 | `tests/test_api.py` → `test_tc06…`、`test_tc08…` |

**驗收條件**

1. 關鍵字出現在標題或描述中，都能找到該回報。
2. 同一個關鍵字用不同英文大小寫搜尋，結果相同。
3. 搜尋沒有結果時，顯示明確的「找不到符合的回報」訊息。
4. 清除搜尋後回到完整列表。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-40](https://sidspaces.atlassian.net/browse/CM-40) | 記錄 Sprint 2 的客戶需求，精修 Story 並重新估點 | 規劃 | 陳萬祥（PO） |
| [CM-41](https://sidspaces.atlassian.net/browse/CM-41) | 在資料庫查詢中實作標題與描述的不分大小寫關鍵字搜尋 | 實作 | 龔國煌 |
| [CM-42](https://sidspaces.atlassian.net/browse/CM-42) | 串接搜尋框、無結果訊息與「清除條件」 | 實作 | 陳萬祥 |
| [CM-43](https://sidspaces.atlassian.net/browse/CM-43) | 測試標題命中、描述命中、大小寫、無結果 | 測試 | 劉智丞 |

### S8　Filter Reports by Location（依地點篩選回報）　`CM-12`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要依地點篩選回報，以便找到相關校園區域的問題。 |
| 優先級 | High。Sprint 2 地點篩選需求，可縮小搜尋範圍。 |
| Story Points | 2（Jira 現有估點） |
| Sprint | 2 |
| Jira 狀態 | 完成 |
| 負責人 | 陳萬祥（畫面）＋龔國煌（查詢） |
| 相依 | S2；與 S7 聯測 |
| 程式位置 | `db.py` → `list_reports`、`list_locations`；`app.py` → `list_locations`；`static/js/student.js` → `loadLocations`；`README.md` 搜尋與篩選說明 |
| 測試位置 | `tests/test_api.py` → `test_tc07…`、`test_tc11…`、`test_locations_endpoint…` |

**驗收條件**

1. 只設定地點時，顯示的每一筆回報都屬於該地點。
2. 同時設定關鍵字和地點時，回報必須兩者都符合才會顯示（AND）。
3. 清除地點後，仍保留的關鍵字繼續有效；全部清除後回到完整列表。
4. 組合篩選的規則在頁面上和 README 中都有說明。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-44](https://sidspaces.atlassian.net/browse/CM-44) | 統一地點的儲存與比對方式（以完整地點名稱比對） | 規劃 | 陳萬祥（PO）、龔國煌 |
| [CM-45](https://sidspaces.atlassian.net/browse/CM-45) | 在資料庫查詢中實作地點篩選與 AND 組合 | 實作 | 龔國煌 |
| [CM-46](https://sidspaces.atlassian.net/browse/CM-46) | 串接地點輸入框，提示已存在的地點；在頁面說明規則 | 實作 | 陳萬祥 |
| [CM-47](https://sidspaces.atlassian.net/browse/CM-47) | 測試只有地點、關鍵字加地點（AND） | 測試 | 劉智丞 |
| [CM-48](https://sidspaces.atlassian.net/browse/CM-48) | 在 README 說明組合篩選的行為 | 文件 | 劉智丞 |

---

## Epic 3｜Staff Resolution Management（Staff 處理管理）

**說明**　經授權的 Staff 可以檢視回報、記錄處理進度，並填寫備註後結案。學生不能執行 Staff 的更新動作。

### S9　Access Staff Functions as an Authorized User（以授權身分使用 Staff 功能）　`CM-13`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要管理功能有存取限制，以便只有經授權的 Staff 能變更回報狀態。 |
| 優先級 | Highest。伺服器端權限控管是 Staff 更新的必要條件。 |
| Story Points | 5（Jira 現有估點） |
| Sprint | 2 |
| Jira 狀態 | 完成 |
| 負責人 | 張廷碩（主責），龔國煌協作 |
| 相依 | 無；S4～S6 依賴它 |
| 程式位置 | `app.py` → `login`、`logout`、`me`、`current_user`、`staff_required`、`staff_page`；`db.py` → `DEMO_USERS`、`users` 資料表；`templates/login.html`；`static/js/login.js` |
| 測試位置 | `tests/test_api.py` → `test_tc10…`、`test_tc12…`、`test_role_comes_from_the_server…`、`test_login_logout_and_wrong_password`、`test_passwords_are_stored_hashed` |

**驗收條件**

1. Staff 示範帳號可以登入，登入後可使用 Staff 功能。
2. 學生帳號直接呼叫更新 API 時回傳 HTTP 403，回報資料不變。
3. 未登入者直接呼叫更新 API 時回傳 HTTP 401，回報資料不變。
4. 角色由伺服器依登入帳號判定，不採信瀏覽器送來的任何內容。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-25](https://sidspaces.atlassian.net/browse/CM-25) | 建立示範帳號，密碼雜湊保存並設定角色 | 實作 | 張廷碩 |
| [CM-26](https://sidspaces.atlassian.net/browse/CM-26) | 實作登入、登出與 session | 實作 | 張廷碩 |
| [CM-27](https://sidspaces.atlassian.net/browse/CM-27) | 加入統一的伺服器端 Staff 檢查，供所有更新路由使用 | 實作 | 張廷碩、龔國煌 |
| [CM-28](https://sidspaces.atlassian.net/browse/CM-28) | 製作登入頁，錯誤訊息清楚易懂 | 實作 | 張廷碩 |
| [CM-29](https://sidspaces.atlassian.net/browse/CM-29) | 測試 Staff、學生、未登入三種身分呼叫更新 API 與開啟管理頁 | 測試 | 劉智丞 |

### S4　View Reports as Staff（以 Staff 身分查看回報）　`CM-8`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要在管理畫面看到回報，以便選擇要處理的案件。 |
| 優先級 | High。Staff 要先選取案件才能更新。 |
| Story Points | 2（Jira 現有估點） |
| Sprint | 2 |
| Jira 狀態 | 完成 |
| 負責人 | 張廷碩 |
| 相依 | S2、S9 |
| 程式位置 | `app.py` → `staff_page`；`templates/staff.html`；`static/js/staff.js` → `loadReports`、`selectReport`、`showReport`；`static/css/staff.css` |
| 測試位置 | `tests/test_api.py` → `test_tc12_staff_page_access_by_role` |

**驗收條件**

1. Staff 登入後可進入管理頁，看到共用資料庫中的回報。
2. 每一筆至少顯示回報 ID、標題和目前狀態，可以選取並打開回報內容。
3. 學生帳號或未登入者無法開啟管理頁（被拒絕或導向登入頁）。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-30](https://sidspaces.atlassian.net/browse/CM-30) | 製作 Staff 管理頁，含回報列表與選取功能 | 實作 | 張廷碩 |
| [CM-31](https://sidspaces.atlassian.net/browse/CM-31) | 在伺服器端依角色保護 `/staff` 頁面 | 實作 | 張廷碩 |
| [CM-32](https://sidspaces.atlassian.net/browse/CM-32) | 測試 Staff、學生、未登入三種身分開啟管理頁 | 測試 | 劉智丞 |

### S5　Update Report Status（更新回報狀態）　`CM-9`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要更新回報的狀態，以便學生知道問題正在處理中。 |
| 優先級 | High。這是記錄處理進度的核心。 |
| Story Points | 2（Jira 現有估點） |
| Sprint | 2 |
| Jira 狀態 | 完成 |
| 負責人 | 張廷碩（主責），龔國煌協作 |
| 相依 | S4、S9 |
| 程式位置 | `app.py` → `update_status`；`db.py` → `update_status`、`STATUSES`；`static/js/staff.js` → 狀態表單 |
| 測試位置 | `tests/test_api.py` → `test_tc05…`、`test_tc09…`、`test_tc13_invalid_status…`、`test_tc04…` |

**驗收條件**

1. Staff 可以把 `Submitted` 的回報改為 `In Progress`。
2. 更新後，學生重新開啟同一個 ID 會看到新狀態。重新啟動應用程式後狀態仍在。
3. 送入 `Submitted`、`In Progress`、`Resolved` 以外的狀態值時，回傳錯誤，回報資料不變。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-33](https://sidspaces.atlassian.net/browse/CM-33) | 實作 `PATCH /api/reports/<id>/status`，驗證狀態值是否合法 | 實作 | 龔國煌、張廷碩 |
| [CM-34](https://sidspaces.atlassian.net/browse/CM-34) | 在管理頁加入狀態選單與儲存結果訊息 | 實作 | 張廷碩 |
| [CM-35](https://sidspaces.atlassian.net/browse/CM-35) | 測試更新、更新後的學生畫面、非法狀態、重啟 | 測試 | 劉智丞 |

### S6　Resolve a Report with a Note（填寫備註後結案）　`CM-10`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要在結案時記錄處理備註，以便學生知道問題是如何處理的。 |
| 優先級 | High。作業規定結案時必須填寫備註。 |
| Story Points | 5（Jira 現有估點） |
| Sprint | 2 |
| Jira 狀態 | 完成 |
| 負責人 | 張廷碩 |
| 相依 | S5、S9 |
| 程式位置 | `app.py` → `update_status`（備註驗證）；`static/js/staff.js` → `validateStatusUpdate`；`static/js/student.js` → `showDetails`（顯示備註） |
| 測試位置 | `tests/test_api.py` → `test_tc09…`、`test_failed_resolve_keeps_an_existing_note`、`test_tc04…`；`tests/student.test.mjs`（Staff 兩項） |

**驗收條件**

1. Staff 填寫非空白的備註後可將回報設為 `Resolved`，狀態與備註一併保存。
2. 沒有備註、備註為空字串或只有空白時無法結案，原狀態與既有備註不變。
3. 學生的詳情畫面顯示 `Resolved` 與處理備註，重新啟動應用程式後兩者仍在。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| [CM-36](https://sidspaces.atlassian.net/browse/CM-36) | 結案時在伺服器端要求去除空白後非空的 `resolution_note` | 實作 | 張廷碩、龔國煌 |
| [CM-37](https://sidspaces.atlassian.net/browse/CM-37) | 選擇「已解決 Resolved」時顯示備註欄位並提示錯誤 | 實作 | 張廷碩 |
| [CM-38](https://sidspaces.atlassian.net/browse/CM-38) | 測試有效備註、缺少備註、純空白備註 | 測試 | 劉智丞 |
| [CM-39](https://sidspaces.atlassian.net/browse/CM-39) | 測試學生端看得到備註，包含重啟之後 | 測試 | 劉智丞 |

---

## Task｜專案協作、流程與交件

Task 與 Story 同層，不計入 28 個 Story Points。下表為 Jira 截至 2026 年 11 月 19 日的工作狀態；「已記錄」不代表原定活動都已實際舉行。

| Task | Jira | 工作內容 | 主責 | 狀態與紀錄 |
| --- | --- | --- | --- | --- |
| T1 | [CM-49](https://sidspaces.atlassian.net/browse/CM-49) | 團隊分工與工作協議 | 龔國煌（SM） | 待辦；已補分工與協議範本，原始正式協議未核實 |
| T2 | [CM-50](https://sidspaces.atlassian.net/browse/CM-50) | Backlog 排序與估點 | 陳萬祥（PO） | 待辦；28 點估點與排序已記錄，Planning Poker 原始投票未核實 |
| T3 | [CM-51](https://sidspaces.atlassian.net/browse/CM-51) | GitHub 程式整合及交叉審查 | 劉智丞 | 待辦；已補整合與審查檢查表，跨人審查證據待確認 |
| T4 | [CM-52](https://sidspaces.atlassian.net/browse/CM-52) | Sprint 1 規劃 | 龔國煌（SM）、陳萬祥（PO） | 完成 |
| T5 | [CM-53](https://sidspaces.atlassian.net/browse/CM-53) | Sprint 1 Review 與 Retrospective | 龔國煌（SM） | 待辦；已補事後回顧，Daily／跨組試用與正式會議未核實 |
| T6 | [CM-54](https://sidspaces.atlassian.net/browse/CM-54) | Sprint 2 搜尋需求與規劃 | 陳萬祥（PO）、龔國煌（SM） | 完成 |
| T7 | [CM-55](https://sidspaces.atlassian.net/browse/CM-55) | 測試紀錄與缺陷複測 | 劉智丞 | 完成；TC01～TC14 均通過，CM-59 複測通過 |
| T8 | [CM-56](https://sidspaces.atlassian.net/browse/CM-56) | Sprint 2 Review 與最終回顧 | 龔國煌（SM） | 待辦；已補事後回顧，正式會議證據未核實 |
| T9 | [CM-57](https://sidspaces.atlassian.net/browse/CM-57) | 五頁團隊報告與四位組員個人心得 | 全員 | 完成 |
| T10 | [CM-58](https://sidspaces.atlassian.net/browse/CM-58) | Demo 排演、備援影片與交件檢查 | 全員 | 待辦；已完成腳本，影片／排演與連結驗證待確認 |

### Sprint 執行結果

| Sprint | Jira 期間 | Sprint Goal | Story | 結果 | 生命週期狀態 |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 | 2026/11/03～11/10 | 學生能提交校園問題，並查看已保存的回報與處理狀態 | CM-5～CM-7 | 3/3，9 點 | Closed（2026/11/18） |
| Sprint 2 | 2026/11/10～11/17 | 學生能搜尋與篩選回報，Staff 可查看、更新並結案 | CM-8～CM-13 | 6/6，19 點 | Closed（2026/11/18） |

兩個正式 Sprint 均已關閉，9 張 Story 全部完成。正式 Sprint 以 Jira 編號與名稱為準；看板中另有一個未開始的 Sprint 2 同名延伸項目，不計入以上完成率。

### 測試結果

| 測試類型 | 主要內容 | 結果 |
| --- | --- | --- |
| Python 自動化測試 | Flask API、輸入驗證、權限、資料保存與重啟 | 41 項通過 |
| JavaScript 自動化測試 | 表單、搜尋參數與備註驗證 | 7 項通過 |
| Chromium 整合與回歸測試 | TC01～TC13 及延遲回應回歸測試 EX01 | 13＋1 項通過 |
| Windows／Chrome 人工測試 | TC01～TC14：學生、Staff、權限、重啟與競態條件 | 14 項通過 |

詳細紀錄參見 [`TEST_RECORD.md`](TEST_RECORD.md)，測試截圖位於 [`evidence/test-evidence/`](evidence/test-evidence/)。

### Bug CM-59｜Staff 快速切換案件

- **問題：** Staff 先選 #1、再選 #2；若 #1 較晚回應，可能顯示或更新錯誤案件。
- **修正：** 僅採用最後選取案件的回應；新案件尚未載入完成前不得沿用舊儲存目標。
- **證據：** 程式索引 `ea6d278`，自動化回歸 EX01 與人工 TC14 複測通過。
- **結果：** 受控延遲下最後停留並更新 #2，#1 資料不變。
- **Jira：** [CM-59](https://sidspaces.atlassian.net/browse/CM-59)，狀態為「完成」。

---

## Definition of Done（完成準則）

團隊定義的完成準則為：功能已整合並可正常運作、符合 Acceptance Criteria、通過相應測試、經非作者的組員審查，且程式與測試證據可追溯，沒有妨礙主要流程的已知缺陷。

Jira 工作狀態與證據完整性分開檢查：9 張 Story 雖已標為完成，但個別 PR 的交叉審查證據仍需以實際紀錄確認；CM-51 因此保留待辦。未實際完成的會議、外組測試與備援影片不得以文件範本代替執行紀錄。
