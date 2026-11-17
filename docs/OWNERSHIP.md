# CampusFix｜分工與程式對照

每張 Story 由誰負責、對應哪段程式和測試。連結固定在 commit `18b8d88`，之後程式修改也不會跑掉。

**這份是分工規劃，不是貢獻紀錄。** 真正的貢獻紀錄是每位組員用自己的 GitHub 帳號提交的 commit 和 PR。

| 代號 | 成員 | 負責範圍 |
| --- | --- | --- |
| A | 陳萬祥 | Product Owner（PO）、學生畫面 |
| B | 龔國煌 | Scrum Master（SM）、後端與資料庫 |
| C | 張廷碩 | 開發者：Staff 與權限 |
| D | 劉智丞 | 開發者：整合與測試 |

## S1 提交問題回報（CF-4）— 龔國煌、陳萬祥

- 後端驗證：[app.py validate_report](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L32-L45)、[app.py create_report](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L100-L109)
- 資料庫：[db.py SCHEMA](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L22-L41)、[db.py create_report](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L82-L90)
- 表單：[templates/index.html](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/templates/index.html)、[student.js 送出表單](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/student.js#L223-L262)
- 測試（劉智丞）：[test_tc01～tc04](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L63-L121)、[test_restart.py](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_restart.py)

## S2 查看報修列表（CF-5）— 陳萬祥

- 後端：[app.py list_reports](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L111-L115)、[db.py list_reports](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L92-L112)
- 畫面：[student.js loadReports](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/student.js#L163-L190)
- 測試（劉智丞）：[test_list_is_empty／tc05](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L125-L141)

## S3 查看報修詳情與狀態（CF-6）— 陳萬祥

- 後端：[app.py get_report](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L117-L120)
- 畫面：[student.js showDetails](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/student.js#L198-L221)
- 測試（劉智丞）：[test_tc05、tc13](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L129-L147)

## S4 Staff 查看報修（CF-7）— 張廷碩

- 後端：[app.py staff_page](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L89-L98)
- 畫面：[templates/staff.html](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/templates/staff.html)、[staff.js 列表與選取](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/staff.js#L92-L172)
- 測試（劉智丞）：[test_tc12_staff_page_access_by_role](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L262-L268)、[e2e_staff_race.cjs](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/e2e_staff_race.cjs)

## S5 更新報修狀態（CF-8）— 張廷碩、龔國煌

- 後端：[app.py update_status](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L128-L149)、[db.py update_status](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L120-L131)
- 畫面：[staff.js 儲存狀態](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/staff.js#L174-L206)
- 測試（劉智丞）：[test_tc13_invalid_status](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L226-L233)

## S6 填寫備註後結案（CF-9）— 張廷碩

- 後端備註檢查：[app.py update_status](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L128-L149)
- 畫面：[staff.js validateStatusUpdate](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/staff.js#L12-L17)
- 測試（劉智丞）：[test_tc09、既有備註保留](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L203-L244)、[student.test.mjs](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/student.test.mjs)

## S7 關鍵字搜尋報修（CF-10）— 龔國煌、陳萬祥

- 後端搜尋：[db.py list_reports](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L92-L112)
- 畫面：[student.js buildReportUrl](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/student.js#L25-L34)
- 測試（劉智丞）：[test_tc06、tc08](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L165-L189)

## S8 依地點篩選報修（CF-11）— 陳萬祥、龔國煌

- 後端：[db.py list_reports](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L92-L112)、[db.py list_locations](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L133-L140)
- 畫面：[student.js loadLocations](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/student.js#L85-L97)
- 說明：[README 第 4 節](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/README.md)
- 測試（劉智丞）：[test_tc07、tc11、locations](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L177-L200)

## S9 Staff 權限控管（CF-12）— 張廷碩、龔國煌

- 權限檢查：[app.py current_user、staff_required](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L63-L79)
- 登入登出：[app.py login／logout／me](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/app.py#L151-L175)、[login.js](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/login.js)
- 示範帳號：[db.py DEMO_USERS](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/db.py#L17-L20)
- 測試（劉智丞）：[test_tc10、tc12、角色與密碼](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/test_api.py#L246-L294)

## Bug：Staff 快速切換存錯報修 — 張廷碩

- 修正：[staff.js selectReport](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/static/js/staff.js#L145-L172)
- 回歸測試：[e2e_staff_race.cjs](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/tests/e2e_staff_race.cjs)
- 紀錄：[BUG_STAFF_STALE_SELECTION.md](https://github.com/sam20060318-star/Campusfix/blob/18b8d88b90d7aa507009e5896b08930080db2343/docs/BUG_STAFF_STALE_SELECTION.md)
