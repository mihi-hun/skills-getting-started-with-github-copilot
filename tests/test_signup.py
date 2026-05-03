"""Tests for the POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_new_student_success(client, new_student_email):
    """Test successful signup of a new student for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_student_email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_student_email in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client, new_student_email):
    """Test that signup adds the participant to the activity's participants list"""
    # Get initial participant count
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    
    # Sign up new student
    client.post(
        "/activities/Chess Club/signup",
        params={"email": new_student_email}
    )
    
    # Check updated participant list
    response = client.get("/activities")
    updated_participants = response.json()["Chess Club"]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert new_student_email in updated_participants


def test_signup_activity_not_found(client, new_student_email):
    """Test signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": new_student_email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up(client, test_email):
    """Test that signing up an already registered student returns 400"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": test_email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_different_activities(client, new_student_email):
    """Test that a student can sign up for multiple different activities"""
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_student_email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": new_student_email}
    )
    assert response2.status_code == 200
    
    # Verify both signups worked
    response = client.get("/activities")
    activities = response.json()
    assert new_student_email in activities["Chess Club"]["participants"]
    assert new_student_email in activities["Programming Class"]["participants"]


def test_signup_case_sensitive_activity_name(client, new_student_email):
    """Test that activity names are case-sensitive"""
    response = client.post(
        "/activities/chess club/signup",  # lowercase
        params={"email": new_student_email}
    )
    
    assert response.status_code == 404


def test_signup_case_sensitive_email(client):
    """Test that email addresses are case-sensitive in participants list"""
    email1 = "NewStudent@mergington.edu"
    email2 = "newstudent@mergington.edu"
    
    # Sign up with first email
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    # Try to sign up with different-case email
    response2 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email2}
    )
    assert response2.status_code == 200  # Should succeed since case differs
    
    # Verify both are in participants list
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert email1 in participants
    assert email2 in participants
