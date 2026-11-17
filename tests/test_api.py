"""Integration tests against the real Flask app and a real SQLite file.

Test names carry the test-case IDs used in docs/TEST_RECORD.md (TC01-TC13).
Run with:  python -m pytest -v
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import db  # noqa: E402
from app import create_app  # noqa: E402

VALID = {
    "title": "Broken projector",
    "location": "Classroom A101",
    "category": "Classroom equipment",
    "description": "The projector will not start.",
}


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "campusfix.db"


@pytest.fixture
def client(db_path):
    return create_app(db_path).test_client()


def submit(client, **overrides):
    response = client.post("/api/reports", json={**VALID, **overrides})
    assert response.status_code == 201, response.get_json()
    return response.get_json()


def login(client, username, password):
    return client.post("/api/login", json={"username": username, "password": password})


def staff_client(db_path):
    client = create_app(db_path).test_client()
    assert login(client, "staff", "staff123").status_code == 200
    return client


def student_client(db_path):
    client = create_app(db_path).test_client()
    assert login(client, "student", "student123").status_code == 200
    return client


def set_status(client, report_id, **body):
    return client.patch(f"/api/reports/{report_id}/status", json=body)


# ---------- S1 Submit a problem report ----------

# Jira CF-4｜S1 提交問題回報
def test_tc01_valid_submission_saves_four_fields_with_id_and_submitted(client):
    created = submit(client)
    assert isinstance(created["id"], int)
    assert created["status"] == "Submitted"
    saved = client.get(f"/api/reports/{created['id']}").get_json()
    for field, value in VALID.items():
        assert saved[field] == value
    assert saved["status"] == "Submitted"
    assert saved["resolution_note"] == ""


# Jira CF-4｜S1 提交問題回報
@pytest.mark.parametrize("field", ["title", "location", "category", "description"])
@pytest.mark.parametrize("bad", ["", "   ", None, 123])
def test_tc02_missing_or_blank_field_is_rejected_and_nothing_is_saved(client, field, bad):
    body = {**VALID, field: bad}
    if bad is None:
        del body[field]
    response = client.post("/api/reports", json=body)
    assert response.status_code == 400
    data = response.get_json()
    assert data["errors"][field].startswith("請輸入")
    assert data["error"] == data["errors"][field]
    assert client.get("/api/reports").get_json() == []


def test_tc02_non_json_body_is_rejected(client):
    assert client.post("/api/reports", data="not json").status_code == 400
    assert client.get("/api/reports").get_json() == []


# Jira CF-4｜S1 提交問題回報
def test_tc03_separate_reports_get_different_ids(client):
    first = submit(client, title="First")
    second = submit(client, title="Second")
    assert first["id"] != second["id"]
    assert client.get(f"/api/reports/{first['id']}").get_json()["title"] == "First"
    assert client.get(f"/api/reports/{second['id']}").get_json()["title"] == "Second"


# ---------- Persistence ----------

# Jira CF-4｜S1 提交問題回報
def test_tc04_reports_and_updates_survive_application_restart(db_path):
    first_run = staff_client(db_path)
    report = submit(first_run)
    assert set_status(first_run, report["id"], status="Resolved", resolution_note="Lamp replaced.").status_code == 200

    restarted = create_app(db_path).test_client()  # a new app on the same database file
    saved = restarted.get(f"/api/reports/{report['id']}").get_json()
    assert saved["title"] == VALID["title"]
    assert saved["status"] == "Resolved"
    assert saved["resolution_note"] == "Lamp replaced."
    assert [item["id"] for item in restarted.get("/api/reports").get_json()] == [report["id"]]


def test_reinitialising_the_database_keeps_existing_reports(db_path, client):
    report = submit(client)
    db.init_db(db_path)
    assert db.seed_demo_reports(db_path) == 0
    assert db.get_report(db_path, report["id"])["title"] == VALID["title"]


# ---------- S2 / S3 List and details ----------

# Jira CF-5｜S2 查看報修列表
def test_list_is_empty_before_any_report(client):
    assert client.get("/api/reports").get_json() == []


# Jira CF-6｜S3 查看報修詳情與狀態
def test_tc05_list_and_details_agree_and_show_latest_status(db_path, client):
    report = submit(client)
    listed = client.get("/api/reports").get_json()
    assert [(item["id"], item["title"], item["status"]) for item in listed] == [
        (report["id"], VALID["title"], "Submitted")
    ]
    detail = client.get(f"/api/reports/{report['id']}").get_json()
    assert detail == listed[0]

    assert set_status(staff_client(db_path), report["id"], status="In Progress").status_code == 200
    assert client.get(f"/api/reports/{report['id']}").get_json()["status"] == "In Progress"
    assert client.get("/api/reports").get_json()[0]["status"] == "In Progress"


# Jira CF-6｜S3 查看報修詳情與狀態
def test_tc13_unknown_report_id_returns_404(client):
    response = client.get("/api/reports/9999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "找不到這筆報修。"
    assert client.get("/api/reports/abc").status_code == 404


# ---------- S7 / S8 Search and filter ----------

@pytest.fixture
def search_client(client):
    submit(client, title="Projector broken", location="Classroom A101", description="No image on screen.")
    submit(client, title="Screen is blank", location="Library", description="The PROJECTOR lamp is dead.")
    submit(client, title="Wi-Fi keeps dropping", location="Library", description="Connection lost often.")
    submit(client, title="Leaking tap", location="Building B", description="Water on the floor.")
    return client


def titles(client, **params):
    return sorted(item["title"] for item in client.get("/api/reports", query_string=params).get_json())


# Jira CF-10｜S7 關鍵字搜尋報修
def test_tc06_keyword_matches_title_or_description_in_any_letter_case(search_client):
    expected = ["Projector broken", "Screen is blank"]
    assert titles(search_client, keyword="projector") == expected
    assert titles(search_client, keyword="PROJECTOR") == expected
    assert titles(search_client, keyword="pRoJeCtOr") == expected


def test_tc06_keyword_is_literal_not_a_wildcard(search_client):
    assert titles(search_client, keyword="%") == []
    assert titles(search_client, keyword="_") == []


# Jira CF-11｜S8 依地點篩選報修
def test_tc07_location_filter_returns_only_that_location(search_client):
    results = search_client.get("/api/reports", query_string={"location": "Library"}).get_json()
    assert len(results) == 2
    assert {item["location"] for item in results} == {"Library"}
    assert titles(search_client, location="library") == titles(search_client, location="Library")
    assert titles(search_client, location="Lib") == []  # whole location must match


# Jira CF-10｜S7 關鍵字搜尋報修
def test_tc08_no_match_returns_empty_list_and_clearing_restores_all(search_client):
    assert titles(search_client, keyword="elevator") == []
    assert len(titles(search_client)) == 4
    assert len(titles(search_client, keyword="  ", location="")) == 4


# Jira CF-11｜S8 依地點篩選報修
def test_tc11_keyword_and_location_together_use_and(search_client):
    assert titles(search_client, keyword="projector", location="Library") == ["Screen is blank"]
    assert titles(search_client, keyword="tap", location="Library") == []


# Jira CF-11｜S8 依地點篩選報修
def test_locations_endpoint_lists_stored_values_once(search_client):
    submit(search_client, location="library")
    assert search_client.get("/api/locations").get_json() == ["Building B", "Classroom A101", "Library"]


# ---------- S4 / S5 / S6 Staff workflow ----------

# Jira CF-9｜S6 填寫備註後結案
def test_tc09_staff_updates_status_and_must_give_a_note_to_resolve(db_path, client):
    staff = staff_client(db_path)
    report = submit(client)

    response = set_status(staff, report["id"], status="In Progress")
    assert response.status_code == 200
    assert response.get_json()["status"] == "In Progress"

    for bad_note in (None, "", "   \n\t "):
        body = {"status": "Resolved"} if bad_note is None else {"status": "Resolved", "resolution_note": bad_note}
        response = set_status(staff, report["id"], **body)
        assert response.status_code == 400
        assert "處理備註" in response.get_json()["error"]
        unchanged = client.get(f"/api/reports/{report['id']}").get_json()
        assert (unchanged["status"], unchanged["resolution_note"]) == ("In Progress", "")

    response = set_status(staff, report["id"], status="Resolved", resolution_note="  Replaced the lamp.  ")
    assert response.status_code == 200
    seen_by_student = client.get(f"/api/reports/{report['id']}").get_json()
    assert seen_by_student["status"] == "Resolved"
    assert seen_by_student["resolution_note"] == "Replaced the lamp."


# Jira CF-8｜S5 更新報修狀態
def test_tc13_invalid_status_is_rejected_and_data_is_unchanged(db_path, client):
    staff = staff_client(db_path)
    report = submit(client)
    for bad in ("Closed", "resolved", "", None, 5):
        assert set_status(staff, report["id"], status=bad).status_code == 400
    assert client.get(f"/api/reports/{report['id']}").get_json()["status"] == "Submitted"
    assert set_status(staff, 9999, status="In Progress").status_code == 404


# Jira CF-9｜S6 填寫備註後結案
def test_failed_resolve_keeps_an_existing_note(db_path, client):
    staff = staff_client(db_path)
    report = submit(client)
    set_status(staff, report["id"], status="Resolved", resolution_note="Fixed.")
    assert set_status(staff, report["id"], status="Resolved", resolution_note="  ").status_code == 400
    saved = client.get(f"/api/reports/{report['id']}").get_json()
    assert (saved["status"], saved["resolution_note"]) == ("Resolved", "Fixed.")


# ---------- S9 Authorization ----------

def test_tc10_student_account_cannot_update_status(db_path, client):
    report = submit(client)
    student = student_client(db_path)
    response = set_status(student, report["id"], status="Resolved", resolution_note="I fixed it myself.")
    assert response.status_code == 403
    saved = client.get(f"/api/reports/{report['id']}").get_json()
    assert (saved["status"], saved["resolution_note"]) == ("Submitted", "")


def test_tc12_anonymous_update_is_401_and_data_is_unchanged(client):
    report = submit(client)
    response = set_status(client, report["id"], status="In Progress")
    assert response.status_code == 401
    assert client.get(f"/api/reports/{report['id']}").get_json()["status"] == "Submitted"


# Jira CF-7｜S4 Staff 查看報修
def test_tc12_staff_page_access_by_role(db_path, client):
    anonymous = client.get("/staff")
    assert anonymous.status_code == 302
    assert anonymous.headers["Location"].endswith("/login")
    assert student_client(db_path).get("/staff").status_code == 403
    assert staff_client(db_path).get("/staff").status_code == 200


def test_role_comes_from_the_server_not_from_the_request(db_path, client):
    report = submit(client)
    student = student_client(db_path)
    response = student.patch(
        f"/api/reports/{report['id']}/status",
        json={"status": "In Progress", "role": "staff"},
        headers={"X-Role": "staff"},
    )
    assert response.status_code == 403


def test_login_logout_and_wrong_password(client):
    assert login(client, "staff", "wrong").status_code == 401
    assert login(client, "nobody", "staff123").status_code == 401
    assert client.get("/api/me").get_json() == {"authenticated": False}
    assert login(client, "staff", "staff123").get_json() == {"username": "staff", "role": "staff"}
    assert client.get("/api/me").get_json()["role"] == "staff"
    assert client.post("/api/logout").status_code == 200
    assert client.get("/api/me").get_json() == {"authenticated": False}
    assert client.get("/staff").status_code == 302


def test_passwords_are_stored_hashed(db_path, client):
    assert "staff123" not in db.get_user(db_path, "staff")["password_hash"]


def test_student_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'data-api-base="/api/reports"' in response.data
