import pytest
from app import create_app, db
from app.models import Task, Comment

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        task = Task(title="Sample Task")
        db.session.add(task)
        db.session.commit()

    return app.test_client()


def test_add_comment(client):
    response = client.post("/tasks/1/comments", json={"content": "Hello"})
    assert response.status_code == 201
    assert response.json["content"] == "Hello"


def test_add_comment_without_content(client):
    response = client.post("/tasks/1/comments", json={})
    assert response.status_code == 400


def test_list_comments(client):
    client.post("/tasks/1/comments", json={"content": "Hi"})
    response = client.get("/tasks/1/comments")
    assert response.status_code == 200
    assert len(response.json["comments"]) == 1


def test_edit_comment(client):
    client.post("/tasks/1/comments", json={"content": "Old"})
    response = client.put("/comments/1", json={"content": "New"})
    assert response.status_code == 200
    assert response.json["content"] == "New"


def test_delete_comment(client):
    client.post("/tasks/1/comments", json={"content": "Test"})
    response = client.delete("/comments/1")
    assert response.status_code == 200
