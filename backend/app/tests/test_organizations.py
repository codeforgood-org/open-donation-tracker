"""Tests for organization endpoints"""
import pytest
from app.models.organization import Organization


@pytest.fixture
def test_organization(db, test_user):
    """Create a test organization"""
    org = Organization(
        name="Test Charity",
        description="A test organization",
        category="Education",
        ein="12-3456789",
        owner_id=test_user.id,
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def test_create_organization(client, auth_headers):
    """Test creating an organization"""
    response = client.post(
        "/api/organizations",
        headers=auth_headers,
        json={
            "name": "New Charity",
            "description": "Helping people",
            "category": "Healthcare",
            "ein": "98-7654321",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Charity"
    assert data["category"] == "Healthcare"
    assert data["is_verified"] is False


def test_get_organizations(client, test_organization):
    """Test getting all organizations"""
    response = client.get("/api/organizations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(org["name"] == "Test Charity" for org in data)


def test_get_organization_by_id(client, test_organization):
    """Test getting a specific organization"""
    response = client.get(f"/api/organizations/{test_organization.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Charity"
    assert data["id"] == test_organization.id


def test_get_organization_stats(client, test_organization):
    """Test getting organization statistics"""
    response = client.get(f"/api/organizations/{test_organization.id}/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_donations" in data
    assert "donation_count" in data
    assert "donor_count" in data


def test_update_organization(client, auth_headers, test_organization):
    """Test updating an organization"""
    response = client.patch(
        f"/api/organizations/{test_organization.id}",
        headers=auth_headers,
        json={"description": "Updated description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"


def test_delete_organization_unauthorized(client, auth_headers, test_organization):
    """Test that non-admin cannot delete organization"""
    response = client.delete(
        f"/api/organizations/{test_organization.id}",
        headers=auth_headers,
    )
    assert response.status_code == 403
