# tests/test_event_api.py
import sys
from pathlib import Path
import json
import pytest
from flask import Flask

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from routes.event_routes import event_bp  # adjust path if needed
from Database.connection import get_connection

SAMPLE_EVENT = {
    "club_id": "club_sesa",
    "event_name": "Test Event",
    "event_date": "2025-06-10",
    "event_time": "15:00",
    "venue": "Test Venue",
    "mode": "online",
    "event_description": "This is a test event",
    "images": ["http://example.com/image1.jpg"],
    "category": "Test Category",
    "ispublic": 1,
    "meeting_note": ""
}

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(event_bp, url_prefix='/events')

    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_create_event(client):
    response = client.post(
        '/events/create',
        data=json.dumps(SAMPLE_EVENT),
        content_type='application/json'
    )
    assert response.status_code in (200, 201)


def test_list_events_by_club(client):
    # Create sample event first
    client.post(
        '/events/create',
        data=json.dumps(SAMPLE_EVENT),
        content_type='application/json'
    )

    club_id = SAMPLE_EVENT["club_id"]
    response = client.get(f'/events/get_events?club_id={club_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert "events" in data


def test_add_participant(client):
    # Create sample event first
    client.post(
        '/events/create',
        data=json.dumps(SAMPLE_EVENT),
        content_type='application/json'
    )

    # Fetch event id from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM event_management WHERE event_name = %s ORDER BY id DESC LIMIT 1",
        (SAMPLE_EVENT["event_name"],)
    )
    event = cursor.fetchone()
    cursor.close()
    conn.close()

    assert event is not None, "Event not found in DB"
    event_id = event[0]

    participant_data = {
        "club_id": SAMPLE_EVENT["club_id"],
        "event_id": event_id,
        "student_email": "student@example.com"
    }

    response = client.post(
        '/events/add_participant',
        data=json.dumps(participant_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data or "message" in data


def test_delete_event(client):
    # Create sample event first
    client.post(
        '/events/create',
        data=json.dumps(SAMPLE_EVENT),
        content_type='application/json'
    )

    # Fetch event id from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM event_management WHERE event_name = %s ORDER BY id DESC LIMIT 1",
        (SAMPLE_EVENT["event_name"],)
    )
    event = cursor.fetchone()
    cursor.close()
    conn.close()

    assert event is not None, "Event not found in DB"
    event_id = event[0]

    delete_data = {
        "club_id": SAMPLE_EVENT["club_id"],
        "event_id": event_id
    }
    print(delete_data)
    response = client.delete(
        '/events/delete',
        data=json.dumps(delete_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data or "message" in data
