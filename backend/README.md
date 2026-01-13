# PRISM Web Backend - Top Recommendations API

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

### 1. Database Setup

First, create a PostgreSQL database:

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE prism_db;

-- Connect to the database
\c prism_db;

-- Create the recommendations table
CREATE TABLE aws_recommendation_consolidate (
    id BIGSERIAL PRIMARY KEY,
    type TEXT,
    account TEXT,
    region TEXT,
    resource_name TEXT,
    resource_id TEXT,
    service TEXT,
    sub_service TEXT,
    recommendation TEXT,
    description TEXT,
    potential NUMERIC(18, 4),
    actual_cost NUMERIC(18, 4),
    target_cost NUMERIC(18, 4),
    current_configuration TEXT,
    expected_configuration TEXT,
    justifications TEXT,
    tags_json JSONB,
    actionable BOOLEAN,
    risk_level TEXT,
    impact TEXT
);

-- Insert sample data for testing
INSERT INTO aws_recommendation_consolidate
(type, description, potential, actual_cost, target_cost, recommendation)
VALUES
('AWS', 'Recommended to right-size EC2 instance from m5.large to m5.medium', 781.12, 1200.00, 418.88, 'Right-size EC2 instance'),
('AWS', 'Delete unused EBS volume in us-east-1', 650.50, 650.50, 0.00, 'Delete unused volume'),
('Databricks', 'Optimize cluster auto-scaling configuration', 580.00, 1000.00, 420.00, 'Optimize cluster'),
('Snowflakes', 'Reduce warehouse size from X-Large to Large', 520.30, 920.30, 400.00, 'Reduce warehouse size'),
('AWS', 'Migrate to newer generation RDS instance', 480.00, 800.00, 320.00, 'Migrate RDS instance'),
('Google Cloud', 'Delete unattached persistent disks', 450.00, 450.00, 0.00, 'Delete unattached disks');
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/prism_db
```

### 3. Start the Server

```bash
# Make sure you're in the backend directory with venv activated
python main.py

# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Top Recommendations

**Endpoint**: `POST /api/v1/overview/top-updates/top-recommendation`

**Request Payload**:

```json
{
  "platform": "aws"
}
```

**Available platform values**:

- `all_platform` - Get recommendations from all platforms
- `aws` - AWS recommendations only
- `google_cloud` - Google Cloud recommendations only
- `databricks` - Databricks recommendations only
- `snowflakes` - Snowflakes recommendations only

**Response**:

```json
{
  "success_response": {
    "status_code": 200,
    "message": "Data Received Successfully",
    "status": true,
    "data": [
      {
        "platform_name": "AWS",
        "description": "Recommended to right-size EC2 instance from m5.large to m5.medium",
        "value": "Save $781.12"
      }
    ]
  }
}
```

**Error Responses**:

- `400` - Invalid request parameters
- `401` - Authentication failed
- `403` - Account locked
- `404` - Not found
- `429` - Too many requests
- `500` - Internal server error
- `503` - Service unavailable

## Testing in Swagger

1. Open http://localhost:8000/docs
2. Look for the "Top Updates" section
3. Click on `POST /api/v1/overview/top-updates/top-recommendation`
4. Click "Try it out"
5. **Authentication**: Click the lock icon and enter Bearer token (or skip for now if testing locally)
6. Modify the request body with your desired platform
7. Click "Execute"
8. View the response below

## Testing without Authentication (Development Only)

To test without authentication, temporarily modify the endpoint in `src/dashboard/overview/api/top_recommendation_api.py`:

Comment out the `current_user` dependency:

```python
async def get_top_recommendations(
    request: TopRecommendationRequest,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user)  # Comment this line
) -> TopRecommendationResponse:
```

## Project Structure

```
backend/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment variables template
├── .env                            # Your environment variables (create this)
└── src/
    ├── auth/                       # Authentication module
    │   └── dependencies.py         # JWT authentication
    ├── database/                   # Database configuration
    │   ├── base.py                # SQLAlchemy base
    │   └── session.py             # Database session management
    └── dashboard/
        └── overview/
            ├── api/               # API endpoints
            │   └── top_recommendation_api.py
            ├── dao/               # Data access layer
            │   └── top_recommendation_dao.py
            ├── models/            # Database models
            │   └── recommendation.py
            ├── schemas/           # Request/Response schemas
            │   └── top_recommendation_schema.py
            └── service/           # Business logic
                └── top_recommendation_service.py
```

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running
- Check DATABASE_URL in .env file
- Ensure database exists and table is created

### Import Errors

- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use

- Change port in main.py or use: `uvicorn main:app --port 8001`
