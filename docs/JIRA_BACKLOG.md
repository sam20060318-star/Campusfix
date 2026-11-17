# CampusFix｜Jira 完整清單（Epic → Story → Subtask，另加 Task／Bug）

**使用前請注意**

- S1～S9 是組內簡稱。`CF-4、CF-5、CF-6、CF-10、CF-11` 來自 Demo 的 README，其餘 key 請從你們的 Jira 看板抄。
- Story 標題保留英文，因為你們 Jira 上已建好的卡片是英文名稱；其餘內容都是中文，可直接貼上。
- **點數與優先級是提案**。教授要求團隊共同估點，請四人實際做一次 Planning Poker（1／2／3／5／8）再登錄。
- **負責人是角色提案**（A 學生 UI、B 後端與資料、C Staff 與權限、D 整合與測試），請填真實姓名。
- 「程式位置」欄是這份程式碼裡的實際檔案，commit／PR 推上 GitHub 後把連結貼到卡片。
- Subtask 不加 Story Points。卡片要等組員實際執行驗收、另一位組員審查後才能移到 Done。

## 階層總覽

```text
Epic 1  Problem Reporting（問題回報）
  └─ S1  Submit a Problem Report                      (CF-4)   5 點  Sprint 1
Epic 2  Report Tracking and Search（回報追蹤與搜尋）
  ├─ S2  View Report List                             (CF-5)   2 點  Sprint 1
  ├─ S3  View Report Details and Status               (CF-6)   2 點  Sprint 1
  ├─ S7  Search Reports by Keyword                    (CF-10)  3 點  Sprint 2
  └─ S8  Filter Reports by Location                   (CF-11)  2 點  Sprint 2
Epic 3  Staff Resolution Management（Staff 處理管理）
  ├─ S9  Access Staff Functions as an Authorized User (key 待填) 5 點  Sprint 2
  ├─ S4  View Reports as Staff                        (key 待填) 2 點  Sprint 2
  ├─ S5  Update Report Status                         (key 待填) 3 點  Sprint 2
  └─ S6  Resolve a Report with a Note                 (key 待填) 3 點  Sprint 2
Task（與 Story 同層，不估點）  T1～T10
Bug （真的發現才建）
```

Sprint 1 提案 9 點（S1、S2、S3）；Sprint 2 提案 18 點（S9 → S4 → S5 → S6，S7、S8 平行）。

---

## Epic 1｜Problem Reporting（問題回報）

**說明**　學生可以填寫必要資訊回報校園問題，系統會驗證內容並永久保存。

### S1　Submit a Problem Report（提交問題回報）　`CF-4`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要提交校園問題回報，以便 Staff 能夠調查處理。 |
| 優先級 | High。其他所有功能都依賴已保存的回報。 |
| Story Points | 5（提案） |
| Sprint | 1 |
| 負責人 | B（後端）＋ A（表單） |
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
| S1-1 | 建立 `reports` 資料表與 SQLite 儲存，ID 由資料庫產生 | 實作 | B |
| S1-2 | 實作 `POST /api/reports`，在伺服器端驗證四個欄位 | 實作 | B |
| S1-3 | 學生表單串接 API，顯示欄位錯誤、新 ID 與狀態 | 實作 | A |
| S1-4 | 測試有效提交、空白欄位（畫面與直接打 API）、唯一 ID | 測試 | D |
| S1-5 | 測試重新整理與重啟後資料仍在 | 測試 | D |

---

## Epic 2｜Report Tracking and Search（回報追蹤與搜尋）

**說明**　學生可以瀏覽已保存的回報、打開單筆查看詳情與目前狀態，並在新增回報前先搜尋或篩選。

### S2　View Report List（查看回報列表）　`CF-5`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要看到已保存的回報，以便找到某個問題和它的狀態。 |
| 優先級 | High。這是追蹤回報的入口。 |
| Story Points | 2（提案） |
| Sprint | 1 |
| 負責人 | A（主責），B 提供查詢 |
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
| S2-1 | 實作 `GET /api/reports`，回傳已保存的回報，新的在前 | 實作 | B |
| S2-2 | 顯示列表（ID、標題、狀態），以及空狀態與錯誤狀態 | 實作 | A |
| S2-3 | 測試列表與已保存資料一致，包含空列表 | 測試 | D |

### S3　View Report Details and Status（查看回報詳情與狀態）　`CF-6`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要查看單筆回報的詳情與目前狀態，以便追蹤處理進度。 |
| 優先級 | High。學生需要它才能追蹤個別回報。 |
| Story Points | 2（提案） |
| Sprint | 1（Sprint 2 補測 Staff 更新後的狀態） |
| 負責人 | A（主責），B 提供單筆 API |
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
| S3-1 | 實作 `GET /api/reports/<id>`，找不到時回傳 404 | 實作 | B |
| S3-2 | 串接詳情視窗，包含處理備註與錯誤訊息 | 實作 | A |
| S3-3 | 測試詳情與列表一致、404 情況、Staff 更新後的狀態 | 測試 | D |

### S7　Search Reports by Keyword（關鍵字搜尋回報）　`CF-10`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要搜尋回報的標題與描述，以便在提交新回報前確認是否已有人回報。 |
| 優先級 | Sprint 2 起為 High（因應客戶需求調高）。可減少重複回報。 |
| Story Points | 3（提案） |
| Sprint | 2 |
| 負責人 | B（搜尋）＋ A（畫面） |
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
| S7-1 | 記錄 Sprint 2 的客戶需求，精修 Story 並重新估點 | 規劃 | PO |
| S7-2 | 在資料庫查詢中實作標題與描述的不分大小寫關鍵字搜尋 | 實作 | B |
| S7-3 | 串接搜尋框、無結果訊息與「清除條件」 | 實作 | A |
| S7-4 | 測試標題命中、描述命中、大小寫、無結果 | 測試 | D |

### S8　Filter Reports by Location（依地點篩選回報）　`CF-11`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為學生，我想要依地點篩選回報，以便找到相關校園區域的問題。 |
| 優先級 | Sprint 2 起為 High（因應客戶需求調高）。可把搜尋範圍縮小到單一區域。 |
| Story Points | 2（提案） |
| Sprint | 2 |
| 負責人 | A（畫面）＋ B（查詢） |
| 相依 | S2；與 S7 聯測 |
| 程式位置 | `db.py` → `list_reports`、`list_locations`；`app.py` → `list_locations`；`static/js/student.js` → `loadLocations`；`README.md` 第 4 節 |
| 測試位置 | `tests/test_api.py` → `test_tc07…`、`test_tc11…`、`test_locations_endpoint…` |

**驗收條件**

1. 只設定地點時，顯示的每一筆回報都屬於該地點。
2. 同時設定關鍵字和地點時，回報必須兩者都符合才會顯示（AND）。
3. 清除地點後，仍保留的關鍵字繼續有效；全部清除後回到完整列表。
4. 組合篩選的規則在頁面上和 README 中都有說明。

**Subtasks**

| # | Subtask | 類型 | 負責 |
| --- | --- | --- | --- |
| S8-1 | 統一地點的儲存與比對方式（整個名稱相同、不分大小寫） | 規劃 | PO＋B |
| S8-2 | 在資料庫查詢中實作地點篩選與 AND 組合 | 實作 | B |
| S8-3 | 串接地點輸入框，提示已存在的地點；在頁面說明規則 | 實作 | A |
| S8-4 | 測試只有地點、關鍵字加地點（AND） | 測試 | D |
| S8-5 | 在 README 說明組合篩選的行為 | 文件 | D |

---

## Epic 3｜Staff Resolution Management（Staff 處理管理）

**說明**　經授權的 Staff 可以檢視回報、記錄處理進度，並填寫備註後結案。學生不能執行 Staff 的更新動作。

### S9　Access Staff Functions as an Authorized User（以授權身分使用 Staff 功能）　`key 待填`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要管理功能有存取限制，以便只有經授權的 Staff 能變更回報狀態。 |
| 優先級 | High。在它完成之前，不能開放 Staff 更新。 |
| Story Points | 5（提案） |
| Sprint | 2（最先做） |
| 負責人 | C（主責），B 協作 |
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
| S9-1 | 建立示範帳號，密碼雜湊保存並設定角色 | 實作 | C |
| S9-2 | 實作登入、登出與 session | 實作 | C |
| S9-3 | 加入統一的伺服器端 Staff 檢查，供所有更新路由使用 | 實作 | C＋B |
| S9-4 | 製作登入頁，錯誤訊息清楚易懂 | 實作 | C |
| S9-5 | 測試 Staff、學生、未登入三種身分呼叫更新 API 與開啟管理頁 | 測試 | D |

### S4　View Reports as Staff（以 Staff 身分查看回報）　`key 待填`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要在管理畫面看到回報，以便選擇要處理的案件。 |
| 優先級 | High。Staff 要先選取案件才能更新。 |
| Story Points | 2（提案） |
| Sprint | 2 |
| 負責人 | C |
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
| S4-1 | 製作 Staff 管理頁，含回報列表與選取功能 | 實作 | C |
| S4-2 | 在伺服器端依角色保護 `/staff` 頁面 | 實作 | C |
| S4-3 | 測試 Staff、學生、未登入三種身分開啟管理頁 | 測試 | D |

### S5　Update Report Status（更新回報狀態）　`key 待填`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要更新回報的狀態，以便學生知道問題正在處理中。 |
| 優先級 | High。這是記錄處理進度的核心。 |
| Story Points | 3（提案） |
| Sprint | 2 |
| 負責人 | C（主責），B 協作 |
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
| S5-1 | 實作 `PATCH /api/reports/<id>/status`，驗證狀態值是否合法 | 實作 | B＋C |
| S5-2 | 在管理頁加入狀態選單與儲存結果訊息 | 實作 | C |
| S5-3 | 測試更新、更新後的學生畫面、非法狀態、重啟 | 測試 | D |

### S6　Resolve a Report with a Note（填寫備註後結案）　`key 待填`

| 欄位 | 內容 |
| --- | --- |
| 使用者故事 | 身為 Staff，我想要在結案時記錄處理備註，以便學生知道問題是如何處理的。 |
| 優先級 | High。作業規定結案時必須填寫備註。 |
| Story Points | 3（提案） |
| Sprint | 2 |
| 負責人 | C |
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
| S6-1 | 結案時在伺服器端要求去除空白後非空的 `resolution_note` | 實作 | C＋B |
| S6-2 | 選擇「已解決 Resolved」時顯示備註欄位並提示錯誤 | 實作 | C |
| S6-3 | 測試有效備註、缺少備註、純空白備註 | 測試 | D |
| S6-4 | 測試學生端看得到備註，包含重啟之後 | 測試 | D |

---

## Task（與 Story 同層，不估 Story Points）

教授要求的流程與交件工作。若團隊使用 Task，請連結到相關 Story 或 Epic。

| # | Task | 負責 | 連結 |
| --- | --- | --- | --- |
| T1 | 把全體組員加入 Jira，記錄 Working Agreement（溝通方式、審查、可投入時間、做不完如何處理） | SM | 全部 |
| T2 | Planning Poker：共同決定九張 Story 的點數與優先級 | PO＋全員 | S1～S9 |
| T3 | 建立 GitHub repository，推上可執行的骨架，確認每人都能 clone 並啟動 | D | S1 |
| T4 | Sprint 1 Planning：目標、日期、選入的 Story、負責人、相依 | SM＋PO | S1～S3 |
| T5 | Sprint 1 Review（請另一組實際提交並查回一筆回報）與 Retrospective | SM | S1～S3 |
| T6 | Sprint 2 Planning：記錄搜尋需求、保留／延後／簡化的取捨、新目標 | PO＋SM | S4～S9 |
| T7 | 執行測試紀錄（至少 10 個案例）並附上證據 | D＋全員 | S1～S9 |
| T8 | Sprint 2 Review、最終 Retrospective、最終看板、未完成工作與已知缺陷 | SM | 全部 |
| T9 | 團隊報告（最多 5 頁）與個人反思（每人 200–300 字） | 全員 | 全部 |
| T10 | 排演 7 分鐘 Demo，錄製備援影片（最多 4 分鐘） | 全員 | 全部 |

Daily Scrum 不建卡，每個工作日留一則團隊筆記（進度／下一步／障礙）。

## Sprint 設定

| Sprint | 目標（可直接貼） | 選入 |
| --- | --- | --- |
| Sprint 1 | 學生可以提交回報，並查回已保存的詳情與目前狀態。 | S1、S2、S3 |
| Sprint 2 | 學生可以在新增回報前先搜尋既有回報，Staff 可以處理回報並結案。 | S9、S4、S5、S6、S7、S8，加上 Sprint 1 的回饋 |

日期請填實際日期。教授要求兩個各一週的 Sprint，若時程不足要先問老師，不能事後回填。

## Bug 範本（真的發現缺陷才建）

```text
摘要：        [簡短描述]
相關 Story：  [Jira key]
嚴重度：      Blocker / Major / Minor
重現步驟：    1. …  2. …  3. …
預期結果：    …
實際結果：    …
證據：        [截圖或 log]
修正：        [commit 或 PR 連結]
複測：        [日期、測試者、Pass/Fail]
```

## Definition of Done（貼到 Jira 專案說明）

一張 Story 要同時符合以下條件才算 Done：功能已在整合後的應用程式中運作、通過全部驗收條件、經另一位組員審查、附有程式與測試證據的連結，而且沒有妨礙正常使用的已知缺陷。
