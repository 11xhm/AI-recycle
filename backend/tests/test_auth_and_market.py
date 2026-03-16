from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from main import create_app


def _client(tmp_path: Path) -> TestClient:
    settings.db_path = (tmp_path / "app.db").resolve()
    settings.upload_dir = (tmp_path / "uploads").resolve()
    settings.ai_mock = True
    settings.ai_provider = "mock"
    app = create_app()
    return TestClient(app)


def test_register_login_me_and_update(tmp_path: Path):
    with _client(tmp_path) as client:
        r = client.post("/api/auth/register", json={"username": "user1", "password": "secret1", "display_name": "n1"})
        assert r.status_code == 200
        token = r.json()["access_token"]

        me = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["username"] == "user1"

        upd = client.patch("/api/me", json={"display_name": "new"}, headers={"Authorization": f"Bearer {token}"})
        assert upd.status_code == 200

        me2 = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
        assert me2.json()["display_name"] == "new"

        login = client.post("/api/auth/login", json={"username": "user1", "password": "secret1"})
        assert login.status_code == 200


def test_listing_create_list_purchase_and_history(tmp_path: Path):
    with _client(tmp_path) as client:
        seller = client.post("/api/auth/register", json={"username": "seller", "password": "secret1"}).json()["access_token"]
        buyer = client.post("/api/auth/register", json={"username": "buyer", "password": "secret1"}).json()["access_token"]

        img = b"abc" * 5000
        files = {"file": ("t.jpg", img, "image/jpeg")}
        data = {"description": "demo", "price": ""}
        created = client.post("/api/listings", files=files, data=data, headers={"Authorization": f"Bearer {seller}"})
        assert created.status_code == 200, created.text
        listing_id = created.json()["id"]

        listed = client.get("/api/listings")
        assert listed.status_code == 200
        assert any(it["id"] == listing_id for it in listed.json())

        purchase = client.post(f"/api/listings/{listing_id}/purchase", headers={"Authorization": f"Bearer {buyer}"})
        assert purchase.status_code == 200

        after = client.get("/api/listings")
        assert all(it["id"] != listing_id for it in after.json())

        history = client.get("/api/history", headers={"Authorization": f"Bearer {buyer}"})
        assert history.status_code == 200
        assert len(history.json()["purchases"]) == 1


def test_recognize_writes_history_when_authed(tmp_path: Path):
    with _client(tmp_path) as client:
        token = client.post("/api/auth/register", json={"username": "user2", "password": "secret1"}).json()["access_token"]
        img = b"xyz" * 2000
        res = client.post(
            "/api/recognize",
            files={"file": ("t.jpg", img, "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 200
        hist = client.get("/api/history", headers={"Authorization": f"Bearer {token}"})
        assert hist.status_code == 200
        assert len(hist.json()["recognitions"]) == 1
