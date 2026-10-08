from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_quiz_validation():
    from quiz_module import _validate_quiz

    quiz = [
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
        },
        {
            "question": "Which is a planet?",
            "options": ["Sun", "Earth", "Moon", "Asteroid"],
            "answer": "Earth",
        },
        {
            "question": "Water freezes at?",
            "options": ["0°C", "50°C", "100°C", "-100°C"],
            "answer": "0°C",
        },
    ]

    assert len(_validate_quiz(quiz)) == 3
