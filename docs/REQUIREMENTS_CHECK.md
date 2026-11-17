# CampusFix｜教授要求對照表

依據教授作業單（4 頁）逐條對照。日期：2026-11-15。

- **已完成並實測**：程式碼已有，且自動化測試與瀏覽器實跑都通過。
- **待團隊**：程式碼做不到，必須由真人完成（Jira 活動、審查、會議、報告、影片）。

## 結論

**程式功能：教授第 2 節的五項最低功能全部涵蓋，沒有缺項。**
**交件：還缺的全部是「人」的部分**，共 12 項，列在第 3 節。其中最要緊的是 Sprint 時程（教授要求兩個各一週）和 Definition of Done 裡的同儕審查。

## 1. 產品功能（作業單第 2 節，配分 25）

| 教授要求 | 狀態 | 在哪裡 | 驗證 |
| --- | --- | --- | --- |
| 儲存 title、location、category、description | 已完成並實測 | `db.py` `reports` 表、`POST /api/reports` | TC01 |
| 驗證必填欄位 | 已完成並實測 | 前端 `validateReport` + 後端 `validate_report`（純空白也擋） | TC02 |
| 產生唯一 report ID | 已完成並實測 | SQLite `AUTOINCREMENT` | TC03 |
| 列表、詳情、目前狀態 | 已完成並實測 | `GET /api/reports`、`GET /api/reports/<id>`、學生頁 | TC05、TC13 |
| Staff 畫面改狀態：Submitted／In Progress／Resolved | 已完成並實測 | `/staff`、`PATCH /api/reports/<id>/status` | TC09、TC13 |
| 結案必填 resolution note | 已完成並實測 | 後端 trim 後不得為空；前端同步提示 | TC09 |
| 關鍵字搜尋 title／description，不分大小寫 | 已完成並實測 | `db.list_reports` | TC06、TC08 |
| 依 location 篩選 | 已完成並實測 | `db.list_reports` | TC07 |
| 說明組合篩選如何運作 | 已完成 | 學生頁列表上方說明文字、README 第 4 節（AND） | TC11 |
| 重新整理與重啟後資料仍在 | 已完成並實測 | SQLite 檔 `instance/campusfix.db` | TC04（真的停掉再啟動行程） |
| Staff 更新只限 staff 角色 | 已完成並實測 | `staff_required`，伺服器端檢查；未登入 401、學生 403 | TC10、TC12 |
| 示範帳號、虛構資料 | 已完成 | `staff/staff123`、`student/student123`；`--seed-demo` | README 第 2 節 |

不必做也沒做：學校 SSO、寄信、AI 功能、照片上傳、公開部署。

## 2. 交件中程式碼已備好的部分

| 教授要求 | 狀態 | 檔案 |
| --- | --- | --- |
| README 含精確安裝／啟動步驟、示範帳號 | 已完成 | `README.md` |
| 至少 10 個測試案例，涵蓋指定的 10 類 | 自動化已執行 13 類；**人工版待團隊執行** | `docs/TEST_RECORD.md` |
| 九張 Story、每張至少三條可測驗收條件、優先級與理由 | 文字已備好，**待貼入並核對 Jira** | `docs/JIRA_BACKLOG.md` |
| 三個 Epic | 文字已備好 | 同上 |
| implementation／testing Subtasks | 文字已備好 | 同上 |
| 註明 AI 協助 | README 第 11 節有草稿，**請改成你們的實際情況** | `README.md` |

## 3. 仍缺、必須由團隊完成的項目

| # | 教授要求（作業單節次） | 要做什麼 |
| --- | --- | --- |
| 1 | 兩個各一週的 Sprint（§7、§8） | 今天 11/15，若 11/19 交件，時間不夠兩週。**請 SM 立刻問老師**能否縮短。不可事後回填日期。 |
| 2 | Team estimate（§5） | 四人實際 Planning Poker。文件裡的點數只是提案。 |
| 3 | Working Agreement、全員加入 Jira（§4） | 記錄溝通、審查、可用時間、做不完怎麼辦。 |
| 4 | 每人可驗證的技術貢獻（§4、§12，個人 10 分） | **目前程式是一次產出的，四人都還沒有 commit。** 請依 A／B／C／D 分工各自讀懂、分支提交對應檔案並互相審查，每人要能解釋自己的部分。 |
| 5 | Definition of Done：另一位組員審查、附程式與測試連結（§6） | 每張 Story 都要有真人 review 和連結後才可移 Done。現在九張都**不能**標 Done。 |
| 6 | commit／PR 標題帶 Jira key（§7） | 例：`CF-4 Save submitted reports`。 |
| 7 | 每個工作日的 Daily Scrum 筆記（§7） | 進度、下一步、障礙。 |
| 8 | Sprint 1 Review：請另一組實際提交並查回一筆（§7） | 記錄回饋與 Goal 是否達成。 |
| 9 | Sprint 1 Retro 選一項改進，Sprint 2 套用並舉例（§7、§8） | 要有真實例子。 |
| 10 | Sprint 2：記錄搜尋需求變更、保留／延後／簡化的取捨、新 Goal、最終 Retro（§8） | S7／S8 修改前後的優先級、驗收、點數。 |
| 11 | 人工執行測試紀錄並簽名；真實缺陷建 Jira Bug（§10） | `docs/TEST_RECORD.md` Part B。Part A 的 tester 是自動化，不是組員。 |
| 12 | 團隊報告（最多 5 頁）、個人反思（每人 200–300 words）、7 分鐘 Demo、備援影片（最多 4 分鐘）、GitHub 與 Jira 連結老師可開（§11） | 尚未開始。 |

## 4. 需要團隊確認的設計決定

程式裡已做了選擇，作業單沒有規定，請確認是否同意。

| 決定 | 目前做法 | 若要改 |
| --- | --- | --- |
| 地點比對 | 整個地點名稱相同才算，不分大小寫；輸入框會提示已存在的地點 | 想要「部分符合」改 `db.list_reports` 一行 |
| 學生是否要登入 | 不用登入就能提交與查詢；只有 Staff 更新受限 | 作業單只要求限制 Staff 更新 |
| 狀態能否倒退 | Staff 可設成三種狀態中任一個；從 Resolved 改回其他狀態會清空備註 | 想禁止重開，在 `app.update_status` 加判斷 |
| 分類 | 前端四個中文選項（教室設備、設施、Wi-Fi 與資訊、其他），後端接受任何非空字串 | 想嚴格限制可在後端加白名單 |
| 介面語言 | 網站為繁體中文；狀態值保存為英文，畫面顯示「已提交 Submitted」這種中英並列 | 想只顯示中文或英文，改 `student.js` 與 `staff.js` 的 `STATUS_LABELS` |
| 記憶體預覽伺服器 | 未放進整合版，避免兩份資料來源 | 原 ZIP 仍可單獨使用 |

## 5. 7 分鐘 Demo 對應

| Demo 要展示 | 操作 |
| --- | --- |
| Validation | 空白表單直接送出 → 四個欄位各自提示 |
| Submit | 填完送出 → 顯示 ID 與 Submitted |
| Retrieve | 列表找到 → View details |
| Search | 關鍵字換大小寫；加上地點示範 AND；查無結果 |
| Resolve | Staff 登入 → In Progress → 空白備註被擋 → 填備註結案 → 學生端看到 |
| Persistence | Ctrl+C 停掉，重新 `python app.py`，資料還在 |
| 追一張 Story | 建議 S6：Jira 卡 → `app.py` `update_status` → `test_tc09…` |
