# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

The API uses JWT (JSON Web Token) for authentication.

### Get Token

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using Tokens

Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register User
- **POST** `/auth/register`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "password123"
  }
  ```

#### Login
- **POST** `/auth/login`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

#### Get Current User
- **GET** `/auth/me`
- **Auth:** Required
- **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
  ```

### Organizations

#### List Organizations
- **GET** `/organizations`
- **Query Parameters:**
  - `category` (optional): Filter by category
  - `verified_only` (optional): Show only verified organizations
  - `skip` (optional): Pagination offset
  - `limit` (optional): Items per page

#### Get Organization
- **GET** `/organizations/{id}`

#### Create Organization
- **POST** `/organizations`
- **Auth:** Required
- **Body:**
  ```json
  {
    "name": "Charity Name",
    "description": "Description",
    "category": "Education",
    "ein": "12-3456789",
    "email": "contact@charity.org",
    "website": "https://charity.org"
  }
  ```

#### Get Organization Stats
- **GET** `/organizations/{id}/stats`
- **Response:**
  ```json
  {
    "total_donations": 50000.0,
    "donation_count": 150,
    "donor_count": 75,
    "active_campaigns": 3,
    "transparency_score": 95.5
  }
  ```

### Campaigns

#### List Campaigns
- **GET** `/campaigns`
- **Query Parameters:**
  - `organization_id` (optional): Filter by organization
  - `active_only` (optional): Show only active campaigns

#### Get Campaign
- **GET** `/campaigns/{id}`

#### Create Campaign
- **POST** `/campaigns`
- **Auth:** Required
- **Body:**
  ```json
  {
    "name": "Campaign Name",
    "description": "Description",
    "goal_amount": 10000.0,
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59",
    "organization_id": 1
  }
  ```

#### Get Campaign Progress
- **GET** `/campaigns/{id}/progress`
- **Response:**
  ```json
  {
    "campaign_id": 1,
    "name": "Campaign Name",
    "goal_amount": 10000.0,
    "current_amount": 7500.0,
    "percentage": 75.0,
    "donor_count": 42,
    "days_remaining": 30,
    "is_active": true
  }
  ```

### Donations

#### List My Donations
- **GET** `/donations`
- **Auth:** Required

#### List All Donations (Public)
- **GET** `/donations/all`
- **Query Parameters:**
  - `organization_id` (optional)
  - `campaign_id` (optional)

#### Create Donation
- **POST** `/donations`
- **Auth:** Required
- **Body:**
  ```json
  {
    "amount": 100.0,
    "currency": "USD",
    "payment_method": "credit_card",
    "organization_id": 1,
    "campaign_id": 1,
    "is_anonymous": false
  }
  ```

#### Get Donation Stats
- **GET** `/donations/stats`
- **Query Parameters:**
  - `organization_id` (optional)
- **Response:**
  ```json
  {
    "total_amount": 150000.0,
    "donation_count": 500,
    "average_donation": 300.0,
    "largest_donation": 5000.0,
    "by_status": {
      "completed": 480,
      "pending": 20
    },
    "by_payment_method": {
      "credit_card": 350,
      "paypal": 100,
      "bank_transfer": 50
    }
  }
  ```

### Impact Reports

#### List Impact Reports
- **GET** `/impact-reports`
- **Query Parameters:**
  - `organization_id` (optional)

#### Get Impact Report
- **GET** `/impact-reports/{id}`

#### Create Impact Report
- **POST** `/impact-reports`
- **Auth:** Required
- **Body:**
  ```json
  {
    "title": "Q1 2024 Impact Report",
    "description": "Summary of our impact",
    "period_start": "2024-01-01T00:00:00",
    "period_end": "2024-03-31T23:59:59",
    "metrics": {
      "people_helped": 1000,
      "meals_provided": 5000,
      "schools_built": 2
    },
    "organization_id": 1
  }
  ```

## Error Responses

All endpoints return standard HTTP status codes:

- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **422**: Validation Error
- **500**: Internal Server Error

Error response format:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

Current implementation does not include rate limiting. For production deployment, consider adding rate limiting middleware.

## Pagination

List endpoints support pagination:
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum items to return (default: 20, max: 100)

## Interactive Documentation

Visit http://localhost:8000/api/docs for interactive API documentation (Swagger UI).
