# 🚀 PRISM Web API - SERVER IS RUNNING!

## ✅ Server Status: ACTIVE

The FastAPI server is now running in **MOCK MODE** (no database required).

### 📍 Access Points

| Service                   | URL                          |
| ------------------------- | ---------------------------- |
| **Swagger UI** (Test API) | http://localhost:8000/docs   |
| **ReDoc** (Documentation) | http://localhost:8000/redoc  |
| **Health Check**          | http://localhost:8000/health |

---

## 🎯 API Endpoint

### Top Recommendations API

**URL:** `POST http://localhost:8000/api/v1/overview/top-updates/top-recommendation`

---

## 🧪 How to Test in Swagger

### Step-by-Step Instructions:

1. **Open Swagger UI**

   - Navigate to: http://localhost:8000/docs
   - You should see the interactive API documentation

2. **Find the Endpoint**

   - Look for the section **"Top Updates"**
   - Find: `POST /api/v1/overview/top-updates/top-recommendation`

3. **Try it Out**

   - Click on the endpoint to expand it
   - Click the **"Try it out"** button

4. **Test with Different Platforms**

   **Test 1 - AWS Only:**

   ```json
   {
     "platform": "aws"
   }
   ```

   **Test 2 - All Platforms:**

   ```json
   {
     "platform": "all_platform"
   }
   ```

   **Test 3 - Databricks:**

   ```json
   {
     "platform": "databricks"
   }
   ```

   **Test 4 - Snowflakes:**

   ```json
   {
     "platform": "snowflakes"
   }
   ```

   **Test 5 - Google Cloud:**

   ```json
   {
     "platform": "google_cloud"
   }
   ```

5. **Execute**

   - Click the **"Execute"** button
   - Scroll down to see the response

6. **View Response**
   - You should see a response like:
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

---

## 📝 Test with cURL

```bash
curl -X POST "http://localhost:8000/api/v1/overview/top-updates/top-recommendation" \
  -H "Content-Type: application/json" \
  -d '{"platform": "aws"}'
```

---

## 📝 Test with Python

```python
import requests

url = "http://localhost:8000/api/v1/overview/top-updates/top-recommendation"
payload = {"platform": "aws"}

response = requests.post(url, json=payload)
print(response.json())
```

---

## 📝 Test with Postman

1. **Method:** POST
2. **URL:** `http://localhost:8000/api/v1/overview/top-updates/top-recommendation`
3. **Headers:**
   - `Content-Type: application/json`
4. **Body (raw JSON):**
   ```json
   {
     "platform": "aws"
   }
   ```

---

## 🔧 Available Platform Filters

| Platform Value | Description                                |
| -------------- | ------------------------------------------ |
| `all_platform` | Returns recommendations from all platforms |
| `aws`          | Returns only AWS recommendations           |
| `google_cloud` | Returns only Google Cloud recommendations  |
| `databricks`   | Returns only Databricks recommendations    |
| `snowflakes`   | Returns only Snowflakes recommendations    |

---

## ✅ Expected Response Structure

```json
{
  "success_response": {
    "status_code": 200,
    "message": "Data Received Successfully",
    "status": true,
    "data": [
      {
        "platform_name": "AWS",
        "description": "Recommendation description here",
        "value": "Save $XXX.XX"
      }
    ]
  }
}
```

---

## 🛑 Error Responses

### Invalid Platform (400)

```json
{
  "status_code": 400,
  "error": "INVALID_REQUEST",
  "message": "Invalid request parameters",
  "details": "Platform must be one of: all_platform, google_cloud, aws, databricks, snowflakes"
}
```

### Server Error (500)

```json
{
  "status_code": 500,
  "error": "INTERNAL_SERVER_ERROR",
  "message": "An unexpected error occurred",
  "details": "Please try again later or contact support"
}
```

---

## 📊 Mock Data Overview

The API currently returns these mock recommendations:

1. **AWS** - Right-size EC2 instance: **Save $781.12**
2. **AWS** - Delete unused EBS volume: **Save $750.50**
3. **Databricks** - Optimize cluster auto-scaling: **Save $680.00**
4. **Snowflakes** - Reduce warehouse size: **Save $620.30**
5. **AWS** - Migrate RDS instance: **Save $580.00**
6. **Google Cloud** - Delete unattached disks: **Save $550.00**

---

## 🔄 Switching to Real Database

To use PostgreSQL instead of mock data:

1. Install PostgreSQL
2. Run `database_setup.sql`
3. Update `.env` with your database credentials
4. Use `python main.py` instead of `python main_mock.py`

---

## ⚙️ Server Controls

- **Stop Server:** Press `CTRL+C` in the terminal
- **Restart Server:** Run the command again
- **View Logs:** Check the terminal where the server is running

---

## 🎉 You're All Set!

The API is ready to test. Open http://localhost:8000/docs and start exploring!
