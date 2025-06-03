# tests/test_club_api.py
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from flask import json
from routes.club_routes import club_bp
from Database.connection import get_connection
import pytest

SAMPLE_CLUB = {
    "id": "test_club_real",
    "title": "Test Club Real",
    "welcome_msg": "Welcome!",
    "welcome_short_para": "Short intro",
    "about_club": "This is a test club",
    "our_activities": "Testing, coding, more testing",
    "additional_information": "No additional info",
    "images_url": {
        "header image": "https://example.com/header.jpg",
        "footer image": "https://example.com/footer.jpg"
    }
}

@pytest.fixture
def client():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(club_bp, url_prefix="/clubs")
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    # Cleanup after each test
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clubs WHERE id = %s", (SAMPLE_CLUB["id"],))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Teardown cleanup failed:", str(e))


def test_create_club_real_db(client):
    response = client.post(
        '/clubs/',
        data=json.dumps(SAMPLE_CLUB),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert "message" in response.get_json()


def test_get_club_real_db(client):
    # Ensure club is created first
    client.post(
        '/clubs/',
        data=json.dumps(SAMPLE_CLUB),
        content_type='application/json'
    )

    response = client.get(f'/clubs/{SAMPLE_CLUB["id"]}')
    assert response.status_code == 200
    assert response.get_json()["id"] == SAMPLE_CLUB["id"]


def test_list_clubs_real_db(client):
    # Ensure club is created first
    client.post(
        '/clubs/',
        data=json.dumps(SAMPLE_CLUB),
        content_type='application/json'
    )

    response = client.get('/clubs/list')
    assert response.status_code == 200
    clubs = response.get_json().get("clubs", [])
    assert any(club["id"] == SAMPLE_CLUB["id"] for club in clubs)
