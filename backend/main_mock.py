"""
PRISM Web Backend - Main Application (Mock Version for Testing).
This version uses mock data instead of a real database.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="PRISM Web API (Mock Mode)",
    description="Backend API for PRISM Web Dashboard - Cost Optimization Platform (Running with Mock Data)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import mock router
from src.dashboard.overview.api.top_recommendation_api_mock import router as mock_router

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "prism-web-backend",
        "mode": "MOCK (No Database Required)",
        "message": "Using mock data for testing. Install PostgreSQL for production use."
    }


# Include mock router
app.include_router(mock_router, prefix="/api/v1")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 PRISM Web API Server Starting (MOCK MODE)")
    print("="*70)
    print("📊 Using MOCK DATA - No database required")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("🎯 Top Recommendations: POST http://localhost:8000/api/v1/overview/top-updates/top-recommendation")
    print("="*70 + "\n")
    
    uvicorn.run(
        "main_mock:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
