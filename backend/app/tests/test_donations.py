"""Tests for donation endpoints"""
import pytest
from app.models.organization import Organization
from app.models.campaign import Campaign
from datetime import datetime, timedelta


@pytest.fixture
def test_organization(db, test_user):
    """Create a test organization"""
    org = Organization(
        name="Test Charity",
        description="A test organization",
        category="Education",
        owner_id=test_user.id,
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@pytest.fixture
def test_campaign(db, test_organization):
    """Create a test campaign"""
    campaign = Campaign(
        name="Test Campaign",
        description="A test campaign",
        goal_amount=10000.0,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        organization_id=test_organization.id,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def test_create_donation(client, auth_headers, test_organization):
    """Test creating a donation"""
    response = client.post(
        "/api/donations",
        headers=auth_headers,
        json={
            "amount": 100.0,
            "currency": "USD",
            "payment_method": "credit_card",
            "organization_id": test_organization.id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.0
    assert data["currency"] == "USD"
    assert data["status"] == "completed"
    assert "transaction_id" in data


def test_create_donation_with_campaign(client, auth_headers, test_organization, test_campaign):
    """Test creating a donation for a specific campaign"""
    response = client.post(
        "/api/donations",
        headers=auth_headers,
        json={
            "amount": 50.0,
            "currency": "USD",
            "payment_method": "paypal",
            "organization_id": test_organization.id,
            "campaign_id": test_campaign.id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 50.0
    assert data["campaign_id"] == test_campaign.id


def test_get_my_donations(client, auth_headers):
    """Test getting user's donations"""
    response = client.get("/api/donations", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_donation_stats(client):
    """Test getting donation statistics"""
    response = client.get("/api/donations/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_amount" in data
    assert "donation_count" in data
    assert "average_donation" in data


def test_create_donation_unauthorized(client, test_organization):
    """Test that unauthenticated user cannot create donation"""
    response = client.post(
        "/api/donations",
        json={
            "amount": 100.0,
            "organization_id": test_organization.id,
        },
    )
    assert response.status_code == 401
