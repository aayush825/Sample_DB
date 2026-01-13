"""
Overview module router.
Aggregates all overview-related API routes.
"""
from fastapi import APIRouter
from src.dashboard.overview.api import top_recommendation_router

router = APIRouter(
    prefix="/overview",
    tags=["Overview"]
)

# Include top recommendation routes
router.include_router(top_recommendation_router)
