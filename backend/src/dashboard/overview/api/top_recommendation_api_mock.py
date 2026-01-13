"""
Mock API routes for Top Recommendations (no database required).
"""
from fastapi import APIRouter, HTTPException, status
import logging

from src.dashboard.overview.dao.top_recommendation_dao_mock import TopRecommendationDAOMock
from src.dashboard.overview.service.top_recommendation_service import TopRecommendationService
from src.dashboard.overview.schemas.top_recommendation_schema import (
    TopRecommendationRequest,
    TopRecommendationResponse,
    InvalidRequestError,
    UnauthorizedError,
    InternalServerError,
    ServiceUnavailableError
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/overview/top-updates",
    tags=["Top Updates"]
)


# Mock database session class
class MockDB:
    """Mock database session."""
    pass


@router.post(
    "/top-recommendation",
    response_model=TopRecommendationResponse,
    summary="Get Top Recommendations (Mock Data)",
    description="Fetch top 6 recommendations based on potential cost savings using MOCK DATA",
    responses={
        200: {
            "description": "Successful response with top recommendations",
            "model": TopRecommendationResponse
        },
        400: {
            "description": "Invalid request parameters",
            "model": InvalidRequestError
        },
        500: {
            "description": "Internal server error",
            "model": InternalServerError
        }
    }
)
async def get_top_recommendations(
    request: TopRecommendationRequest
) -> TopRecommendationResponse:
    """
    Get top 6 recommendations based on potential cost savings (MOCK DATA).
    
    **This endpoint uses mock data and does not require a database.**
    
    **Request Body:**
    - `platform`: Filter by platform - one of: all_platform, google_cloud, aws, databricks, snowflakes
    
    **Returns:**
    - List of top 6 recommendations with platform_name, description, and formatted savings value
    """
    try:
        # Validate platform
        valid_platforms = ["all_platform", "google_cloud", "aws", "databricks", "snowflakes"]
        if request.platform not in valid_platforms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status_code": 400,
                    "error": "INVALID_REQUEST",
                    "message": "Invalid request parameters",
                    "details": f"Platform must be one of: {', '.join(valid_platforms)}"
                }
            )

        # Use mock DAO
        mock_db = MockDB()
        dao = TopRecommendationDAOMock(mock_db)
        
        # Get recommendations
        recommendations = dao.get_top_recommendations(
            platform=request.platform,
            limit=6
        )
        
        # Use service to format response
        from src.dashboard.overview.schemas.top_recommendation_schema import (
            RecommendationItem,
            SuccessResponse
        )
        
        recommendation_items = []
        for rec in recommendations:
            item = RecommendationItem(
                platform_name=rec.type,
                description=rec.description or rec.recommendation,
                value=f"Save ${rec.potential:,.2f}"
            )
            recommendation_items.append(item)
        
        success_response = SuccessResponse(
            status_code=200,
            message="Data Received Successfully",
            status=True,
            data=recommendation_items
        )
        
        logger.info(
            f"Successfully fetched top recommendations for platform: {request.platform} (MOCK MODE)"
        )
        
        return TopRecommendationResponse(success_response=success_response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching top recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": 500,
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": "Please try again later or contact support"
            }
        )
