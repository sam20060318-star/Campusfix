# CampusFix｜測試紀錄

**分成兩部分。** A 部分是對這份程式碼實際執行過的自動化測試。B 部分是人工測試紀錄，要由組員在瀏覽器實際操作後填寫並簽上自己的名字。請勿未經操作就把 A 部分的結果抄到 B 部分。

Jira key（小組 CF 專案）：S1 `CF-4`、S2 `CF-5`、S3 `CF-6`、S4 `CF-7`、S5 `CF-8`、S6 `CF-9`、S7 `CF-10`、S8 `CF-11`、S9 `CF-12`。

## A 部分：自動化測試

- **日期：** 2026-11-15
- **執行方式：** 開發階段的自動化測試。組員操作結果見 B 部分。
- **指令：** `python -m pytest -v`（41 項通過）與 `node --test tests/student.test.mjs`（7 項通過）
- **環境：** Python 3.13、Flask 3.1、SQLite、Node 22、Linux
- 另外用 Chromium 瀏覽器對真實伺服器走過一次：空白表單送出 → 四個欄位各自顯示「請輸入…」；提交 → 顯示「報修已送出。報修編號 #4。狀態：已提交 Submitted。」；關鍵字 `SOCKET` 加地點 `圖書館` → 一筆結果；`wi-fi` 找到「Wi-Fi 一直斷線」；不存在的關鍵字 → 顯示「找不到符合的報修」；未登入開 `/staff` → 導向 `/login`；學生帳號 → HTTP 403「只有 Staff 可以更新報修。」；Staff 設為處理中、純空白備註被拒「結案時必須填寫處理備註。」、填備註後已解決；學生詳情顯示「已解決 Resolved」與備註；停止伺服器再啟動 → 詳情相同。

| 測試 ID | Story | 自動化測試名稱 | 預期結果 | 實際結果 | 結果 |
| --- | --- | --- | --- | --- | --- |
| TC01 | S1 | `test_tc01_valid_submission_saves_four_fields_with_id_and_submitted` | 回傳 201、整數 ID、`Submitted`，四個欄位讀回後相同 | 與預期相同 | Pass |
| TC02 | S1 | `test_tc02_missing_or_blank_field_is_rejected_and_nothing_is_saved`（16 組輸入）、`test_tc02_non_json_body_is_rejected` | 回傳 400，訊息指出是哪個欄位；列表仍是空的 | 與預期相同 | Pass |
| TC03 | S1 | `test_tc03_separate_reports_get_different_ids` | 兩個不同的 ID，各自查得到 | 與預期相同 | Pass |
| TC04 | S1、S5、S6 | `test_tc04_reports_and_updates_survive_application_restart`、`test_tc04_real_process_restart_keeps_report_status_and_note` | 伺服器行程停止再啟動後，回報、`Resolved` 與備註都不變 | 與預期相同 | Pass |
| TC05 | S2、S3、S5 | `test_tc05_list_and_details_agree_and_show_latest_status` | 列表與詳情內容一致；Staff 更新後兩邊都顯示 `In Progress` | 與預期相同 | Pass |
| TC06 | S7 | `test_tc06_keyword_matches_title_or_description_in_any_letter_case` | `projector`、`PROJECTOR`、`pRoJeCtOr` 都找到「只在標題」和「只在描述」的兩筆 | 與預期相同 | Pass |
| TC07 | S8 | `test_tc07_location_filter_returns_only_that_location` | 只有 `Library` 的回報；`library` 結果相同；`Lib` 沒有結果 | 與預期相同 | Pass |
| TC08 | S7 | `test_tc08_no_match_returns_empty_list_and_clearing_restores_all` | 搜尋 `elevator` 得到空列表；不帶條件時四筆都在 | 與預期相同 | Pass |
| TC09 | CF-7、CF-8、CF-9 | `test_tc09_staff_updates_status_and_must_give_a_note_to_resolve` | `In Progress` 已保存；缺備註、空備註、純空白備註 → 400 且資料不變；有效備註 → `Resolved`，學生看得到 | 與預期相同 | Pass |
| TC10 | CF-12 | `test_tc10_student_account_cannot_update_status` | 回傳 403；狀態仍是 `Submitted`，備註為空 | 與預期相同 | Pass |
| TC11 | S7、S8 | `test_tc11_keyword_and_location_together_use_and` | 只留下兩個條件都符合的那一筆 | 與預期相同 | Pass |
| TC12 | CF-7、CF-12 | `test_tc12_anonymous_update_is_401_and_data_is_unchanged`、`test_tc12_staff_page_access_by_role` | 未登入回傳 401；`/staff`：未登入被導向登入頁、學生 403、Staff 200 | 與預期相同 | Pass |
| TC13 | S3、S5 | `test_tc13_unknown_report_id_returns_404`、`test_tc13_invalid_status_is_rejected_and_data_is_unchanged` | 不存在的 ID 回傳 404；非法狀態回傳 400，資料不變 | 與預期相同 | Pass |

這次執行沒有發現缺陷，所以沒有建立 Bug。

## B 部分：人工測試紀錄（由組員執行）

照 `docs/TESTING_GUIDE.md` 的順序操作。操作後填寫「實際結果」、「Pass/Fail」、「測試者／日期」，截圖存在 `test-evidence`。

- **測試的版本（GitHub commit）：** ＿＿＿＿＿＿
- **測試者：** ＿＿＿＿＿＿　**日期：** ＿＿＿＿＿＿　**環境：** Windows／macOS、Chrome 版本 ＿＿＿＿
- **自動化測試（由測試者親自執行）：** pytest ＿＿ passed、node ＿＿ pass（截圖：`01-pytest.png`、`02-node.png`）

| 測試 ID | Jira key | 步驟／輸入 | 預期結果 | 實際結果 | Pass/Fail | 測試者／日期 |
| --- | --- | --- | --- | --- | --- | --- |
| TC01 | CF-4 | 在 `/` 填標題「麥克風沒聲音」、地點「教室 B205」、分類「教室設備」、描述「講桌的麥克風打開後沒有聲音。」後送出，再打開它的詳情。 | 訊息顯示報修編號與「已提交 Submitted」。詳情顯示相同的四個值。 | | | |
| TC02 | CF-4 | 空白表單直接送出。接著其他欄位正常填、地點只填空白再送出。再用主控台直接對 API 送出空白地點。 | 每個空欄位各自顯示訊息。API 回傳 400。列表沒有新增任何資料。 | | | |
| TC03 | CF-4 | 提交兩筆不同的回報。 | 兩個 ID 不同，各自打開的詳情正確。 | | | |
| TC04 | CF-4、CF-8、CF-9 | 記下 TC09 結案的那筆 ID。重新整理頁面。用 Ctrl+C 停止應用程式，不加 `--seed-demo` 重新啟動，再打開同一筆。 | 重新整理後與重啟後，欄位、`Resolved` 與備註都不變。 | | | |
| TC05 | CF-5、CF-6、CF-8 | 從列表打開一筆「已提交 Submitted」的報修。用 Staff 把它改為「處理中 In Progress」。回學生頁重新打開詳情。 | 詳情與列表內容一致。更新後同一個 ID 顯示「處理中 In Progress」。 | | | |
| TC06 | CF-10 | 先提交一筆標題「螢幕沒有畫面」、地點「圖書館」、描述「The PROJECTOR lamp is dead.」和一筆標題「Projector 故障」、地點「教室 A101」的報修。搜尋 `projector`，再搜尋 `PROJECTOR`。 | 兩次都找到這兩筆。 | | | |
| TC07 | CF-11 | 準備至少兩個不同地點的回報。只輸入地點 `圖書館` 後搜尋。 | 每一筆結果的地點都是圖書館。 | | | |
| TC08 | CF-10 | 搜尋 `zzzz`。接著按「清除條件」。 | 顯示「找不到符合的報修」訊息。清除後恢復完整列表。 | | | |
| TC09 | CF-7、CF-8、CF-9 | 用 `staff` 登入。選一筆報修，狀態選「處理中 In Progress」後按「儲存狀態」。再選「已解決 Resolved」，備註只打空白後儲存。再填入真正的備註後儲存。到學生頁打開該回報。 | 處理中已保存。純空白備註被拒絕，顯示「結案時必須填寫處理備註。」。填備註後變成已解決，學生看得到狀態與備註。 | | | |
| TC10 | CF-12 | 用 `student` 登入後，以主控台送出更新請求（指令見下方）。重新打開該回報。 | HTTP 403。狀態與備註不變。 | | | |
| TC11 | CF-10、CF-11 | 沿用 TC06 的資料。關鍵字 `projector`、地點 `圖書館` 同時填寫後搜尋。 | 只顯示「螢幕沒有畫面」那一筆（兩者都符合）。 | | | |
| TC12 | CF-7、CF-12 | 未登入時開 `/staff`，並在未登入狀態送出更新請求。用 `student` 登入後開 `/staff`。用 `staff` 登入。 | 被導向登入頁；HTTP 401；學生被拒絕（403）；Staff 看得到管理頁。 | | | |
| TC13 | CF-6、CF-8 | 打開 `/api/reports/9999`。用 Staff 身分對更新 API 送出狀態 `Closed`。 | HTTP 404 並有訊息；HTTP 400，回報不變。 | | | |
| TC14 | CF-7、CF-8（Bug CM-59） | 執行 `node tests/e2e_staff_race.cjs`；再手動：Network 設 3G，在 Staff 頁點 #1 後馬上點 #2，改成處理中並儲存。 | 腳本顯示 `PASS`。畫面停在 #2，儲存的是 #2，#1 仍是已提交。 | | | |

### 主控台指令

在網頁按 `F12` → Console 分頁，貼上後按 Enter。如果 Chrome 不讓你貼上，先手動輸入 `allow pasting` 再貼。把 `/1/` 換成實際的回報 ID。

TC02（直接對 API 送出空白地點）：

```javascript
fetch('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:'測試',location:'  ',category:'其他',description:'測試'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

TC10（學生登入後送出）與 TC12（未登入時送出）：

```javascript
fetch('/api/reports/1/status',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'Resolved',resolution_note:'test'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

TC13（Staff 登入後送出非法狀態）：

```javascript
fetch('/api/reports/1/status',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'Closed'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

帳號切換建議：一般視窗用 `staff` 登入；無痕視窗（`Ctrl+Shift+N`）先做「未登入」的測試，再用 `student` 登入做學生的測試。注意 Chrome 所有無痕視窗共用同一個登入狀態，要回到未登入，請把無痕視窗全部關掉再重開。詳細步驟見 `docs/TESTING_GUIDE.md`。

## 缺陷與複測

只記錄真實發現的缺陷，並在 Jira 建立 Bug。沒有發現就讓表格留空。

| Bug key | 發現於 | 嚴重度 | 摘要 | 修正（commit／PR） | 複測結果、測試者、日期 |
| --- | --- | --- | --- | --- | --- |
| CM-59（個人空間；小組 CF 尚未建 Bug） | Staff 管理頁操作 | Major | Staff 先點 #1 再點 #2，較慢回來的 #1 回應把畫面和儲存目標切回 #1，更新寫進 #1 | `static/js/staff.js` 的 `selectReport` 加入點選序號；[commit ea6d278](https://github.com/sam20060318-star/Campusfix/commit/ea6d278667bf8b4594418e133383baae4f6b9ccf) | 2026-11-15 自動化複測 Pass（`tests/e2e_staff_race.cjs`）；組員複測：見 TC14 |

詳細重現步驟與 Bug 草稿見 `docs/BUG_STAFF_STALE_SELECTION.md`。
