"""Tests for the DELETE /activities/{activity_name}/unregister endpoint"""

import pytest


def test_unregister_success(client, test_email):
    """Test successful unregistration from an activity"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": test_email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client, test_email):
    """Test that unregister removes the participant from the activity"""
    # Get initial participant count
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    assert test_email in initial_participants
    
    # Unregister student
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": test_email}
    )
    
    # Check updated participant list
    response = client.get("/activities")
    updated_participants = response.json()["Chess Club"]["participants"]
    assert len(updated_participants) == initial_count - 1
    assert test_email not in updated_participants


def test_unregister_activity_not_found(client, test_email):
    """Test unregister from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": test_email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_signed_up(client):
    """Test that unregistering a student not signed up returns 400"""
    email = "notsignedup@mergington.edu"
    
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]


def test_signup_then_unregister_workflow(client, new_student_email):
    """Test the complete workflow: signup followed by unregister"""
    # Sign up new student
    signup_response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": new_student_email}
    )
    assert signup_response.status_code == 200
    
    # Verify signup worked
    response = client.get("/activities")
    assert new_student_email in response.json()["Soccer Team"]["participants"]
    
    # Unregister student
    unregister_response = client.delete(
        "/activities/Soccer Team/unregister",
        params={"email": new_student_email}
    )
    assert unregister_response.status_code == 200
    
    # Verify unregister worked
    response = client.get("/activities")
    assert new_student_email not in response.json()["Soccer Team"]["participants"]


def test_unregister_then_signup_again(client, new_student_email):
    """Test that a student can sign up after unregistering"""
    activity = "Swimming Club"
    
    # Sign up
    client.post(
        f"/activities/{activity}/signup",
        params={"email": new_student_email}
    )
    
    # Unregister
    client.delete(
        f"/activities/{activity}/unregister",
        params={"email": new_student_email}
    )
    
    # Sign up again
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": new_student_email}
    )
    
    assert response.status_code == 200
    response = client.get("/activities")
    assert new_student_email in response.json()[activity]["participants"]


def test_unregister_case_sensitive_activity_name(client, test_email):
    """Test that activity names are case-sensitive for unregister"""
    response = client.delete(
        "/activities/chess club/unregister",  # lowercase
        params={"email": test_email}
    )
    
    assert response.status_code == 404


def test_unregister_multiple_from_different_activities(client, test_email):
    """Test unregistering from multiple activities"""
    # First, sign up for another activity
    client.post(
        "/activities/Drama Club/signup",
        params={"email": test_email}
    )
    
    # Unregister from Chess Club
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": test_email}
    )
    assert response1.status_code == 200
    
    # Verify still in Drama Club
    response = client.get("/activities")
    activities = response.json()
    assert test_email not in activities["Chess Club"]["participants"]
    assert test_email in activities["Drama Club"]["participants"]
    
    # Unregister from Drama Club
    response2 = client.delete(
        "/activities/Drama Club/unregister",
        params={"email": test_email}
    )
    assert response2.status_code == 200
    
    # Verify not in either
    response = client.get("/activities")
    activities = response.json()
    assert test_email not in activities["Chess Club"]["participants"]
    assert test_email not in activities["Drama Club"]["participants"]
