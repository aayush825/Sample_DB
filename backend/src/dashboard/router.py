"""
Dashboard module router.
Aggregates all dashboard-related API routes.
"""
from fastapi import APIRouter
from src.dashboard.overview import overview_router

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Include overview routes
router.include_router(overview_router)
