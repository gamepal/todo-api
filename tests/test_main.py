from fastapi.testclient import TestClient
from main import app, todos

client = TestClient(app)


def setup_function():
    todos.clear()


def test_create_todo():
    r = client.post("/todos", json={"title": "buy milk"})
    assert r.status_code == 200
    assert r.json()["title"] == "buy milk"
    assert r.json()["done"] is False


def test_list_empty():
    r = client.get("/todos")
    assert r.json() == []


def test_get_not_found():
    r = client.get("/todos/999")
    assert r.status_code == 404