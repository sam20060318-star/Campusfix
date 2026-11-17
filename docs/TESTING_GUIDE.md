# CampusFix｜完整測試步驟（中文介面版）

照順序做，報修編號才會和下面寫的一樣。整套約 45 分鐘，可以四人分著做。

## 第 0 步：準備（只做一次）

1. 解壓縮 `campusfix.zip`，用 VS Code 打開 `campusfix` 資料夾。
2. 選「Terminal → New Terminal」，依序執行：

```bash
py -3 -m venv .venv
```

```bash
.venv\Scripts\Activate.ps1
```

（出現「已停用指令碼執行」時，先執行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 再重跑上一行。成功後終端機開頭會有 `(.venv)`。）

```bash
pip install -r requirements.txt
```

3. 如果之前啟動過舊版，先刪掉 `instance` 資料夾，讓資料從頭開始。

## 第 1 步：自動化測試

```bash
python -m pytest -v
```

預期最後一行：`41 passed`。

```bash
node --test tests/student.test.mjs
```

預期：`# pass 7`、`# fail 0`（沒裝 Node.js 可跳過）。兩個結果都截圖。

## 第 2 步：啟動網站

```bash
python app.py --seed-demo
```

用 Chrome 打開 http://127.0.0.1:5000/ ，應看到 3 筆報修：

| 編號 | 標題 | 地點 |
| --- | --- | --- |
| #1 | 走廊燈故障 | B 棟 |
| #2 | Wi-Fi 一直斷線 | 圖書館 |
| #3 | 投影機無法開機 | 教室 A101 |

這個終端機不要關。

**主控台用法**：按 `F12` → 「Console」分頁 → 貼上指令 → Enter。Chrome 不讓貼上時，先手動輸入 `allow pasting` 再貼。

**視窗安排**：一般視窗當學生頁和 Staff 用；無痕視窗（`Ctrl+Shift+N`）專門做「未登入」和「學生帳號」的測試。

---

## A. 學生功能（一般視窗，不用登入）

### TC01　有效提交（S1）

1. 左邊「回報問題」表單填：
   - 問題標題：`麥克風沒聲音`
   - 地點：`教室 B205`
   - 分類：`教室設備`
   - 問題描述：`講桌的麥克風打開後沒有聲音。`
2. 按「送出報修」。
3. 右邊列表找到這筆，按「查看詳情」。

**預期**：出現「報修已送出。報修編號 #4。狀態：已提交 Submitted。」；詳情的地點、分類、問題描述和填的一樣，狀態「已提交 Submitted」。

### TC02　缺少必填欄位（S1）

1. 什麼都不填，按「送出報修」。
2. 標題、分類、描述正常填，地點只打幾個空白，按「送出報修」。
3. 主控台貼上（模擬繞過畫面直接送 API）：

```javascript
fetch('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:'測試',location:'  ',category:'其他',description:'測試'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

4. 按列表的「重新整理」。

**預期**：步驟 1 四個欄位下各自出現「請輸入標題。」「請輸入地點。」「請輸入分類。」「請輸入問題描述。」；步驟 2 只有地點出現「請輸入地點。」；步驟 3 主控台顯示 `400` 和「請輸入地點。」；步驟 4 仍是 4 筆報修。

### TC03　唯一編號（S1）

1. 提交標題 `測試 A`、地點 `B 棟`、分類 `其他`、描述 `第一筆`。
2. 提交標題 `測試 B`、地點 `B 棟`、分類 `其他`、描述 `第二筆`。
3. 分別按兩筆的「查看詳情」。

**預期**：編號分別是 #5 和 #6，各自的詳情內容正確。

### TC06　關鍵字搜尋，不分大小寫（S7）

1. 先提交兩筆測試資料：
   - 標題 `螢幕沒有畫面`、地點 `圖書館`、分類 `教室設備`、描述 `The PROJECTOR lamp is dead.`（關鍵字只在描述）
   - 標題 `Projector 故障`、地點 `教室 A101`、分類 `教室設備`、描述 `按下電源後沒有反應。`（關鍵字只在標題）
2. 搜尋框輸入 `projector`，按「搜尋」。
3. 改成 `PROJECTOR`，按「搜尋」。

**預期**：兩次都顯示「2 筆報修」，就是這兩筆。

### TC07　地點篩選（S8）

1. 關鍵字清空，地點輸入 `圖書館`，按「搜尋」。

**預期**：顯示「2 筆報修」（Wi-Fi 一直斷線、螢幕沒有畫面），地點都是圖書館。

### TC11　關鍵字加地點採 AND（S7、S8）

1. 關鍵字 `projector`、地點 `圖書館`，按「搜尋」。

**預期**：只剩「螢幕沒有畫面」1 筆。「Projector 故障」（地點不符）和「Wi-Fi 一直斷線」（關鍵字不符）都不出現。

### TC08　查無結果（S7）

1. 地點清空，關鍵字輸入 `zzzz`，按「搜尋」。
2. 按「清除條件」。

**預期**：顯示「找不到符合的報修。請換個關鍵字或地點，或清除條件。」；清除後恢復「8 筆報修」。

---

## B. Staff 功能（一般視窗）

### TC05 + TC09　Staff 更新、學生看到最新狀態、結案必填備註（S2～S6）

1. 學生頁打開 #4「麥克風沒聲音」的詳情，確認是「已提交 Submitted」，關掉詳情。
2. 點上方「Staff 管理」，用 `staff` / `staff123` 登入。
3. 左邊列表點 #4。
4. 狀態選「處理中 In Progress」，按「儲存狀態」。
5. 點上方「學生頁面」，打開 #4 的詳情。
6. 回到 Staff 管理頁，點 #4，狀態選「已解決 Resolved」，處理備註只打幾個空白，按「儲存狀態」。
7. 處理備註改成 `已更換麥克風電池。`，按「儲存狀態」。
8. 回學生頁，打開 #4 的詳情。

**預期**：
- 步驟 4：「已儲存。報修 #4 目前狀態：處理中 In Progress。」
- 步驟 5：學生看到同一筆 #4 變成「處理中 In Progress」（TC05）
- 步驟 6：紅字「結案時必須填寫處理備註。」，狀態沒變
- 步驟 7：「已儲存。報修 #4 目前狀態：已解決 Resolved。」
- 步驟 8：學生看到「已解決 Resolved」和處理備註「已更換麥克風電池。」（TC09）

### TC04　重新整理與重啟後資料仍在（S1、S5、S6）

1. 學生頁按 `F5`，打開 #4 的詳情。
2. 回終端機按 `Ctrl+C` 停止網站。
3. 重新啟動（不要加 `--seed-demo`）：

```bash
python app.py
```

4. 瀏覽器按 `F5`，打開 #4 的詳情，也看一下列表筆數。

**預期**：重新整理和重啟後，#4 的內容、「已解決 Resolved」、處理備註都還在；列表仍是 8 筆。

---

## C. 權限測試（無痕視窗＋主控台）

> Chrome 所有無痕視窗共用同一個登入狀態，所以**先做未登入，再登入學生**。

### TC12（前半）　未登入（S4、S9）

1. 開無痕視窗（`Ctrl+Shift+N`），網址輸入 http://127.0.0.1:5000/staff 。
2. 按 `F12` 開主控台，貼上：

```javascript
fetch('/api/reports/1/status',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'In Progress'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

**預期**：步驟 1 自動跳到登入頁；步驟 2 顯示 `401` 和「請先以 Staff 帳號登入。」。

### TC10　學生不能做 Staff 更新（S9）

1. 同一個無痕視窗，用 `student` / `student123` 登入。
2. 主控台貼上：

```javascript
fetch('/api/reports/1/status',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'Resolved',resolution_note:'我自己修好了'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

3. 網址改成 http://127.0.0.1:5000/ ，打開 #1「走廊燈故障」的詳情。

**預期**：步驟 1 顯示「已用 student 登入，但這不是 Staff 帳號，不能管理報修。」；步驟 2 顯示 `403` 和「只有 Staff 可以更新報修。」；步驟 3 的 #1 仍是「已提交 Submitted」，沒有處理備註。

### TC12（後半）　學生進不了管理頁

1. 同一個無痕視窗，網址改成 http://127.0.0.1:5000/staff 。

**預期**：顯示「你目前以 student 登入，這不是 Staff 帳號。請改用 Staff 帳號登入才能管理報修。」，看不到管理功能。（Staff 能進入已在 TC09 驗證。）

### TC13　不存在的編號與非法狀態（S3、S5）

1. 回到**一般視窗**（已用 staff 登入），網址打開 http://127.0.0.1:5000/api/reports/9999 。
2. 回 Staff 管理頁，主控台貼上：

```javascript
fetch('/api/reports/1/status',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'Closed'})}).then(r=>r.json().then(d=>console.log(r.status,d)))
```

3. 在 Staff 管理頁點 #1。

**預期**：步驟 1 顯示 `{"error":"找不到這筆報修。"}`；步驟 2 顯示 `400` 和「狀態必須是 Submitted、In Progress 或 Resolved。」；步驟 3 的 #1 仍是「已提交 Submitted」。

---

## 記錄方式

- 每做完一個案例，填 `docs/TEST_RECORD.md` B 部分：**實際結果**（看到什麼）、**Pass/Fail**、**測試者／日期**（實際操作者的名字）。
- 每個案例截圖（`Win+Shift+S`），主控台案例要把 Console 輸出一起截進去。
- 建議分工：A 做 TC01～TC03、B 做 TC06～TC08、TC11，C 做 TC05、TC09、TC10、TC12，D 做 TC04、TC13 和自動化測試。
- 結果和預期不同就記 Fail，到 Jira 建 Bug（重現步驟、預期、實際、截圖），修好後複測並記錄。不可以把 Fail 改成 Pass。
- 想從頭重測：`Ctrl+C` 停止網站，刪掉 `instance` 資料夾，再執行 `python app.py --seed-demo`。
