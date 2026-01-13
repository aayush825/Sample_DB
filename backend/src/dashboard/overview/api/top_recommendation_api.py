"""
API routes for Top Recommendations in the Overview/Top Updates module.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from src.database.session import get_db
from src.auth.dependencies import get_current_user
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
    prefix="/top-updates",
    tags=["Top Updates"]
)


@router.post(
    "/top-recommendation",
    response_model=TopRecommendationResponse,
    summary="Get Top Recommendations",
    description="Fetch top 6 recommendations based on potential cost savings (actual_cost - target_cost)",
    responses={
        200: {
            "description": "Successful response with top recommendations",
            "model": TopRecommendationResponse
        },
        400: {
            "description": "Invalid request parameters",
            "model": InvalidRequestError
        },
        401: {
            "description": "Authentication failed",
            "model": UnauthorizedError
        },
        500: {
            "description": "Internal server error",
            "model": InternalServerError
        },
        503: {
            "description": "Service temporarily unavailable",
            "model": ServiceUnavailableError
        }
    }
)
async def get_top_recommendations(
    request: TopRecommendationRequest,
    db: Session = Depends(get_db)
    # current_user: dict = Depends(get_current_user)  # Commented for testing without auth
) -> TopRecommendationResponse:
    """
    Get top 6 recommendations based on potential cost savings.
    
    The recommendations are sorted by the 'potential' field in descending order,
    where potential represents the difference between actual_cost and target_cost.
    
    **Request Body:**
    - `platform`: Filter by platform - one of: all_platform, google_cloud, aws, databricks, snowflakes
    
    **Returns:**
    - List of top 6 recommendations with platform_name, description, and formatted savings value
    
    **Example Response:**
    ```json
    {
        "success_response": {
            "status_code": 200,
            "message": "Data Received Successfully",
            "status": true,
            "data": [
                {
                    "platform_name": "AWS",
                    "description": "Recommended to right-size EC2 instance",
                    "value": "Save $781.12"
                }
            ]
        }
    }
    ```
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

        # Get recommendations from service
        service = TopRecommendationService(db)
        response = service.get_top_recommendations(
            platform=request.platform,
            limit=6  # Top 6 recommendations as per requirement
        )
        
        logger.info(
            f"Successfully fetched top recommendations for platform: {request.platform}"
        )
        
        return response

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
