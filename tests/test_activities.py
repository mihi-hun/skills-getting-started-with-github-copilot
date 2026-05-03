"""Tests for the GET /activities endpoint"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check that all activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Soccer Team" in data
    assert "Swimming Club" in data
    assert "Art Club" in data
    assert "Drama Club" in data
    assert "Math Club" in data
    assert "Science Club" in data


def test_activity_has_required_fields(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    data = response.json()
    
    # Check a single activity has all required fields
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_activity_participants_is_list(client):
    """Test that participants field is a list"""
    response = client.get("/activities")
    data = response.json()
    
    chess_club = data["Chess Club"]
    assert isinstance(chess_club["participants"], list)
    assert len(chess_club["participants"]) > 0


def test_activity_initial_participants(client):
    """Test that activities have the correct initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club should have michael and daniel initially
    chess_participants = data["Chess Club"]["participants"]
    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants


def test_get_activities_response_type(client):
    """Test that GET /activities returns a dictionary/object"""
    response = client.get("/activities")
    data = response.json()
    
    assert isinstance(data, dict)
    assert len(data) == 9  # 9 activities total
