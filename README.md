# PRISM Web Backend - Top Recommendations API

A FastAPI-based REST API for fetching top cost optimization recommendations for cloud platforms (AWS, Databricks, Snowflakes, Google Cloud).

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Environment Variables](#environment-variables)

## ✨ Features

- **Top Recommendations API**: Fetch top 6 cost optimization recommendations based on potential savings
- **Multi-Platform Support**: AWS, Databricks, Snowflakes, Google Cloud
- **Dynamic Calculation**: Potential savings calculated as `actual_cost - target_cost`
- **Mock Mode**: Test without database setup
- **Production Ready**: Full PostgreSQL integration with SQLAlchemy
- **Interactive Documentation**: Swagger UI and ReDoc
- **Authentication**: JWT-based authentication (optional in development)
- **Comprehensive Error Handling**: Structured error responses

## 🛠 Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL with SQLAlchemy 2.0.25
- **Authentication**: PyJWT + python-jose
- **Validation**: Pydantic 2.5.3
- **Server**: Uvicorn with auto-reload
- **Python**: 3.10+

## 📁 Project Structure

```
backend/
├── main.py                              # Production server (with database)
├── main_mock.py                         # Mock server (no database required)
├── requirements.txt                     # Python dependencies
├── database_setup.sql                   # PostgreSQL database setup
├── .env.example                        # Environment variables template
├── README.md                           # Setup guide
├── TESTING_GUIDE.md                    # API testing instructions
├── POSTGRES_SETUP.md                   # Database setup guide
└── src/
    ├── auth/
    │   └── dependencies.py             # JWT authentication
    ├── database/
    │   ├── base.py                    # SQLAlchemy base
    │   └── session.py                 # Database session management
    └── dashboard/
        └── overview/
            ├── api/                   # API endpoints
            │   ├── top_recommendation_api.py      # Production API
            │   └── top_recommendation_api_mock.py # Mock API
            ├── dao/                   # Data Access Layer
            │   ├── top_recommendation_dao.py      # Production DAO
            │   └── top_recommendation_dao_mock.py # Mock DAO
            ├── models/               # Database models
            │   └── recommendation.py
            ├── schemas/              # Request/Response schemas
            │   └── top_recommendation_schema.py
            └── service/              # Business logic
                └── top_recommendation_service.py
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+ (for production)
- Git

### Quick Start (Mock Mode - No Database Required)

1. **Clone the repository**

   ```bash
   git clone https://github.com/aayush825/Sample_DB.git
   cd Sample_DB/backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run mock server (no database needed)**

   ```bash
   python main_mock.py
   ```

5. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Production Setup (With PostgreSQL)

1. **Install PostgreSQL**

   - Download from: https://www.postgresql.org/download/

2. **Create database and tables**

   ```bash
   psql -U postgres
   \i database_setup.sql
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run production server**
   ```bash
   python main.py
   ```

## 📖 API Documentation

### Endpoint

**POST** `/api/v1/overview/top-updates/top-recommendation`

Get top 6 recommendations based on potential cost savings.

### Request Body

```json
{
  "platform": "aws"
}
```

**Available platform values:**

- `all_platform` - All platforms
- `aws` - AWS only
- `databricks` - Databricks only
- `snowflakes` - Snowflakes only
- `google_cloud` - Google Cloud only

### Response (200 OK)

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
      },
      {
        "platform_name": "AWS",
        "description": "Delete unused EBS volume in us-east-1",
        "value": "Save $750.50"
      }
    ]
  }
}
```

### Error Responses

- **400 Bad Request**: Invalid platform parameter
- **401 Unauthorized**: Authentication failed
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service temporarily unavailable

## 🧪 Testing

### Swagger UI (Interactive)

1. Open http://localhost:8000/docs
2. Find **"Top Updates"** section
3. Click **POST /api/v1/overview/top-updates/top-recommendation**
4. Click **"Try it out"**
5. Modify the request body
6. Click **"Execute"**

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/overview/top-updates/top-recommendation" \
  -H "Content-Type: application/json" \
  -d '{"platform": "aws"}'
```

### Python

```python
import requests

url = "http://localhost:8000/api/v1/overview/top-updates/top-recommendation"
payload = {"platform": "all_platform"}

response = requests.post(url, json=payload)
print(response.json())
```

### Postman

1. Method: **POST**
2. URL: `http://localhost:8000/api/v1/overview/top-updates/top-recommendation`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   { "platform": "aws" }
   ```

## 🔧 Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/prism_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
ENVIRONMENT=development

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📊 Database Schema

```sql
CREATE TABLE aws_recommendation_consolidate (
    id BIGSERIAL PRIMARY KEY,
    type TEXT,                          -- Platform type (AWS, Databricks, etc.)
    account TEXT,
    region TEXT,
    resource_name TEXT,
    resource_id TEXT,
    service TEXT,
    sub_service TEXT,
    recommendation TEXT,
    description TEXT,
    potential NUMERIC(18, 4),           -- Can store pre-calculated or NULL
    actual_cost NUMERIC(18, 4) NOT NULL,-- Current cost
    target_cost NUMERIC(18, 4) NOT NULL,-- Optimized cost
    current_configuration TEXT,
    expected_configuration TEXT,
    justifications TEXT,
    tags_json JSONB,
    actionable BOOLEAN,
    risk_level TEXT,
    impact TEXT
);
```

**Note**: The API calculates `potential` dynamically as `actual_cost - target_cost`.

## 📝 Additional Documentation

- [Backend README](backend/README.md) - Detailed setup guide
- [Testing Guide](backend/TESTING_GUIDE.md) - Comprehensive testing instructions
- [PostgreSQL Setup](backend/POSTGRES_SETUP.md) - Database setup guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Author

**Aayush**

- GitHub: [@aayush825](https://github.com/aayush825)

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- SQLAlchemy for the excellent ORM
- Pydantic for data validation

---

**Happy Coding! 🚀**
