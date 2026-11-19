# CampusFix｜測試紀錄

本文件合併原始 `TEST_RECORD.md`、CM 專案整理版與 2026-11-17～18 的實際人工測試結果。保留原始 A／B 兩部分、測試步驟、Console 指令及缺陷複測紀錄。

**Jira 正式專案：CM**  
Story 對應：S1 `CM-5`、S2 `CM-6`、S3 `CM-7`、S4 `CM-8`、S5 `CM-9`、S6 `CM-10`、S7 `CM-11`、S8 `CM-12`、S9 `CM-13`。  
**人工測試者：** 劉智丞　**日期：** 2026-11-17～18  
**本次人工測試環境：** Windows 11、Chrome（版本未記錄）、Python Flask、SQLite、本機 `http://127.0.0.1:5000`。  

## A 部分：自動化測試（原始開發階段紀錄）


- **日期：** 2026-11-16
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
| TC09 | CM-8、CM-9、CM-10 | `test_tc09_staff_updates_status_and_must_give_a_note_to_resolve` | `In Progress` 已保存；缺備註、空備註、純空白備註 → 400 且資料不變；有效備註 → `Resolved`，學生看得到 | 與預期相同 | Pass |
| TC10 | CM-13 | `test_tc10_student_account_cannot_update_status` | 回傳 403；狀態仍是 `Submitted`，備註為空 | 與預期相同 | Pass |
| TC11 | S7、S8 | `test_tc11_keyword_and_location_together_use_and` | 只留下兩個條件都符合的那一筆 | 與預期相同 | Pass |
| TC12 | CM-8、CM-13 | `test_tc12_anonymous_update_is_401_and_data_is_unchanged`、`test_tc12_staff_page_access_by_role` | 未登入回傳 401；`/staff`：未登入被導向登入頁、學生 403、Staff 200 | 與預期相同 | Pass |
| TC13 | S3、S5 | `test_tc13_unknown_report_id_returns_404`、`test_tc13_invalid_status_is_rejected_and_data_is_unchanged` | 不存在的 ID 回傳 404；非法狀態回傳 400，資料不變 | 與預期相同 | Pass |

上述自動化測試執行未發現新缺陷；另有先前發現並修復的 CM-59 Bug，詳見文末缺陷與複測。

## B 部分：人工測試紀錄（由組員執行）

依 `docs/TESTING_GUIDE.md` 與原始測試案例執行。表中維持原案例的測試步驟與預期結果，實際結果則記錄本次實際採用的 ID、輸入與觀察值。兩者不同時，於結果明確註記。

- **測試者：** 劉智丞
- **測試日期：** 2026-11-17～18
- **測試系統：** Flask + SQLite 開發／測試版本
- **本次親自執行的附加腳本：** `node tests/e2e_staff_race.cjs` → PASS
- **本次未重新確認執行：** `python -m pytest -v`、`node --test tests/student.test.mjs`；不將原開發階段數字宣稱為本次結果

| 測試 ID | Jira key | 步驟／輸入 | 預期結果 | 實際結果 | Pass/Fail | 測試者／日期 |
| --- | --- | --- | --- | --- | --- | --- |
| TC01 | CM-5 | 在 `/` 填標題「麥克風沒聲音」、地點「教室 B205」、分類「教室設備」、描述「講桌的麥克風打開後沒有聲音。」後送出，再打開它的詳情。 | 訊息顯示報修編號與「已提交 Submitted」。詳情顯示相同的四個值。 | 已建立 #4「麥克風沒聲音」，狀態 Submitted，詳情與四個輸入欄位一致。 | Pass | 劉智丞／2026-11-17 |
| TC02 | CM-5 | 空白表單直接送出。接著其他欄位正常填、地點只填空白再送出。再用主控台直接對 API 送出空白地點。 | 每個空欄位各自顯示訊息。API 回傳 400。列表沒有新增任何資料。 | 空白表單顯示四個欄位錯誤；空白地點遭拒；直接 POST API 回傳 HTTP 400；當時列表維持 6 筆。 | Pass | 劉智丞／2026-11-17 |
| TC03 | CM-5 | 提交兩筆不同的回報。 | 兩個 ID 不同，各自打開的詳情正確。 | #5「TC03-A 教室燈光故障」及 #6「TC03-B 飲水機故障」為不同 ID；兩筆詳情均與各自內容相符；重新整理後仍保留各自 ID。 | Pass | 劉智丞／2026-11-18 |
| TC04 | CM-5、CM-9、CM-10 | 記下 TC09 結案的那筆 ID。重新整理頁面。用 Ctrl+C 停止應用程式，不加 `--seed-demo` 重新啟動，再打開同一筆。 | 重新整理後與重啟後，欄位、`Resolved` 與備註都不變。 | 依測試者操作停止並重新執行 `python app.py`（非 `--seed-demo`），終端顯示資料庫 `instance/campusfix.db` 及 Flask 在 127.0.0.1:5000 運行；重啟後 #8 仍為 Resolved，原備註與資料保留；另有 #5 Resolved、#2 In Progress 的截圖。 | Pass | 劉智丞／2026-11-18 |
| TC05 | CM-6、CM-7、CM-9 | 從列表打開一筆「已提交 Submitted」的報修。用 Staff 把它改為「處理中 In Progress」。回學生頁重新打開詳情。 | 詳情與列表內容一致。更新後同一個 ID 顯示「處理中 In Progress」。 | 學生頁 #2「Wi-Fi 一直斷線」的列表與詳情均顯示 In Progress，ID、地點、分類、描述一致；先前 Staff 已對 #2 更新狀態（TC14 操作）。 | Pass | 劉智丞／2026-11-18 |
| TC06 | CM-11 | 先提交一筆標題「螢幕沒有畫面」、地點「圖書館」、描述「The PROJECTOR lamp is dead.」和一筆標題「Projector 故障」、地點「教室 A101」的報修。搜尋 `projector`，再搜尋 `PROJECTOR`。 | 兩次都找到這兩筆。 | 中文標題查詢「飲水機」僅得 #6；小寫 `projector` 找到 #7（描述含 `PROJECTOR`）及 #8（標題含 `Projector`）；「反覆中斷」找到 #2。2026-11-18 補測全大寫 `PROJECTOR`，地點留空，搜尋結果為 2 筆（#7、#8），符合預期，確認搜尋不區分英文字母大小寫。 | Pass | 劉智丞／2026-11-18 |
| TC07 | CM-12 | 準備至少兩個不同地點的回報。只輸入地點 `圖書館` 後搜尋。 | 每一筆結果的地點都是圖書館。 | 只輸入地點「圖書館」顯示 #2、#7，兩筆地點皆為圖書館；地點「圖書館 2F」的 #6 未被納入。另測「教室 A101」得 #3、#5、#8，「A101」為 0 筆。 | Pass | 劉智丞／2026-11-18 |
| TC08 | CM-11 | 搜尋 `zzzz`。接著按「清除條件」。 | 顯示「找不到符合的報修」訊息。清除後恢復完整列表。 | 使用不存在的關鍵字 `XYZ999NOTFOUND` 得 0 筆並顯示「找不到符合的報修」；點選「清除條件」後欄位清空、列表恢復 8 筆。與原例 `zzzz` 的字串不同，但已測同一無結果／清除功能。 | Pass（等效測資） | 劉智丞／2026-11-18 |
| TC09 | CM-8、CM-9、CM-10 | 用 `staff` 登入。選一筆報修，狀態選「處理中 In Progress」後按「儲存狀態」。再選「已解決 Resolved」，備註只打空白後儲存。再填入真正的備註後儲存。到學生頁打開該回報。 | 處理中已保存。純空白備註被拒絕，顯示「結案時必須填寫處理備註。」。填備註後變成已解決，學生看得到狀態與備註。 | #8 從 Submitted 改為 In Progress；空備註結案被拒，填寫有效備註後成功 Resolved，Staff 與學生端均可見備註。2026-11-18 補測 #3：先設為 In Progress，再依測試步驟在 Resolved 的處理備註欄輸入三個半形空格並嘗試儲存；頁面顯示「結案時必須填寫處理備註。」；後續 GET `/api/reports/3` 回傳 HTTP 200，`status` 仍為 `In Progress`、`resolution_note` 為空字串，未誤結案。（空白字元輸入依測試者操作，截圖本身無法辨識空格。） | Pass | 劉智丞／2026-11-18 |
| TC10 | CM-13 | 用 `student` 登入後，以主控台送出更新請求（指令見下方）。重新打開該回報。 | HTTP 403。狀態與備註不變。 | student 身分送出 `PATCH /api/reports/1/status`，回傳 HTTP 403「只有 Staff 可以更新報修。」；後續 GET #1 回傳 200，狀態仍 Submitted、resolution_note 為空。 | Pass | 劉智丞／2026-11-18 |
| TC11 | CM-11、CM-12 | 沿用 TC06 的資料。關鍵字 `projector`、地點 `圖書館` 同時填寫後搜尋。 | 只顯示「螢幕沒有畫面」那一筆（兩者都符合）。 | 建立 #7（描述含 PROJECTOR、地點圖書館）與 #8（標題含 Projector、地點教室 A101）；以 `projector` + `圖書館` 搜尋僅顯示 #7（1 筆），正確排除 #8。 | Pass | 劉智丞／2026-11-18 |
| TC12 | CM-8、CM-13 | 未登入時開 `/staff`，並在未登入狀態送出更新請求。用 `student` 登入後開 `/staff`。用 `staff` 登入。 | 被導向登入頁；HTTP 401；學生被拒絕（403）；Staff 看得到管理頁。 | 未登入進入 /staff 轉至 /login；未登入 PATCH 回傳 HTTP 401，#1 不變；student 存取 /staff 回傳 403；staff 存取 /staff 回傳 200 並顯示管理頁。 | Pass | 劉智丞／2026-11-18 |
| TC13 | CM-7、CM-9 | 打開 `/api/reports/9999`。用 Staff 身分對更新 API 送出狀態 `Closed`。 | HTTP 404 並有訊息；HTTP 400，回報不變。 | GET /api/reports/9999 回傳 404；Staff PATCH #1 狀態 `Closed` 回傳 400；再次 GET #1 為 Submitted，備註空白，資料未變。 | Pass | 劉智丞／2026-11-18 |
| TC14 | CM-8、CM-9（Bug CM-59） | 執行 `node tests/e2e_staff_race.cjs`；再手動：Network 設 3G，在 Staff 頁點 #1 後馬上點 #2，改成處理中並儲存。 | 腳本顯示 `PASS`。畫面停在 #2，儲存的是 #2，#1 仍是已提交。 | 執行 `node tests/e2e_staff_race.cjs` 顯示 PASS；Chrome Network 設 3G，先選 #1 隨即選 #2，畫面停留在 #2；儲存後 API 讀回 #2=In Progress、#1=Submitted。 | Pass | 劉智丞／2026-11-18 |


### 人工測試證據索引

| TC | 圖片／證據來源 |
| --- | --- |
| TC01 | 原始紀錄 TC01；首次建立 #4 的對話證據 |
| TC02 | TC02-01-empty-form.png、TC02-02-blank-location.png、TC02-03-api-validation.png |
| TC03 | TC03-01-report-5-details.png、TC03-02-report-6-details.png、TC03-03-unique-ids-after-refresh.png |
| TC04 | TC04-1.png～TC04-3.png（ZIP）；TC04-01-after-restart-list.png、TC04-02-resolved-report-persisted.png、TC04-03-status-persisted.png（後續上傳）；重新啟動 Terminal／#8 Resolved 的對話截圖（尚未核實已歸檔） |
| TC05 | TC05-1.png～TC05-4.png（早期檔名）；#2 學生列表與詳情對話截圖（尚未核實已歸檔） |
| TC06 | TC06-1.png～TC06-3.png（早期檔名）；三次查詢的對話截圖（尚未核實已歸檔）；`download.png`（補測大寫 `PROJECTOR` 命中 #7、#8） |
| TC07 | 「教室 A101」「A101」「圖書館」的三張對話截圖（尚未核實已歸檔） |
| TC08 | 「XYZ999NOTFOUND」與「清除條件」的兩張對話截圖（尚未核實已歸檔） |
| TC09 | TC09-1.png～TC09-3.png（早期紀錄）；#8 五階段對話截圖（尚未核實已歸檔）；`download(1).png`（補測 #3 結案驗證提示）；`download(20261118-140127).png`（GET #3 仍為 In Progress、備註空白） |
| TC10 | student PATCH 403 與 GET #1 不變的對話截圖（尚未核實已歸檔） |
| TC11 | TC11-01-first-report.png、TC11-02-second-report.png、TC11-03-combined-search.png |
| TC12 | TC12-01-anonymous-redirect.png、TC12-02-anonymous-api-401.png、TC12-03-student-forbidden.png、TC12-04-staff-access-200.png |
| TC13 | TC13-01-invalid-report-id.png、TC13-02-invalid-status.png |
| TC14 | TC14-01-race-script-pass.png、TC14-02-last-selected-report.png、TC14-03-final-verification.png |

**執行觀察與驗收差異：**

- **TC08：** 原始例子是 `zzzz`；實測使用 `XYZ999NOTFOUND`，驗證的是同一項「無結果＋清除條件」功能，保留測資差異。
- **TC09：** 原 #8 已驗證空備註遭拒及有效備註結案；補測 #3 時，依操作流程僅輸入三個半形空格，畫面顯示必填提示，API 查詢確認資料仍為 In Progress、備註空白。輸入的空格無法僅由靜態截圖直接辨認，故此步驟依測試者操作紀錄佐證。
- **TC04：** 終端截圖顯示重新執行 `python app.py`、SQLite 資料庫路徑，測試者確認先前已停止 Flask；重啟後查看 #8 仍是 Resolved 且備註保留。沒有證據顯示曾執行 `--seed-demo`，但不宣稱有獨立錄影捕捉整段重啟過程。
- **TC12：** 原始案例只要求未登入／student／staff 角色存取及 401/403/200；未另外執行「登出後 Session 立即失效」的獨立測試，不能憑此紀錄宣稱已驗證該情境。

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

此表保留原始 CM 專案已有的 Bug 紀錄；`2026-11-15` 的自動化執行未發現**新增** Bug，不代表整個開發過程沒有發現 Bug。

| Bug key | 發現於 | 嚴重度 | 摘要 | 修正（commit／PR） | 複測結果、測試者、日期 |
| --- | --- | --- | --- | --- | --- |
| CM-59 | Staff 管理頁操作 | Major | Staff 先點 #1 再點 #2，較慢回來的 #1 回應可能覆蓋最後選取的報修及儲存目標。 | `static/js/staff.js` 的 `selectReport` 加入點選序號；[commit ea6d278](https://github.com/sam20060318-star/Campusfix/commit/ea6d278667bf8b4594418e133383baae4f6b9ccf) | 2026-11-18：`node tests/e2e_staff_race.cjs` 輸出 `PASS staff page keeps the last clicked report and saves to it`；3G 手動快速切換後停留 #2，更新 #2 為 In Progress，API 查詢確認 #1 仍 Submitted（劉智丞）。 |

詳細重現步驟與 Bug 草稿：`docs/BUG_STAFF_STALE_SELECTION.md`。

## 結論

- **14 項人工案例均已完成並記錄為 Pass**（TC06、TC09 已於 2026-11-18 補測；TC08 使用等效無結果測資）。TC09 純空格輸入依測試者操作紀錄，並以畫面驗證訊息及 API 狀態未變作為結果證據。
- 原歷史自動化測試保留原紀錄的結果，與本次個人執行的 TC14 Playwright 測試分開列示。
