"""
Service layer for Top Recommendations.
Handles business logic for fetching and formatting top recommendations.
"""
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session

from src.dashboard.overview.dao.top_recommendation_dao import TopRecommendationDAO
from src.dashboard.overview.schemas.top_recommendation_schema import (
    RecommendationItem,
    SuccessResponse,
    TopRecommendationResponse
)


class TopRecommendationService:
    """Service class for Top Recommendation operations."""

    def __init__(self, db: Session):
        """Initialize the service with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.dao = TopRecommendationDAO(db)

    @staticmethod
    def _format_savings(potential: Decimal) -> str:
        """
        Format potential savings as a display string.
        
        Args:
            potential: The potential savings amount
            
        Returns:
            Formatted string like 'Save $781.12'
        """
        if potential is None:
            return "Save $0.00"
        return f"Save ${potential:,.2f}"

    @staticmethod
    def _get_platform_display_name(platform_type: str) -> str:
        """
        Get display-friendly platform name.
        
        Args:
            platform_type: The platform type from database
            
        Returns:
            Display-friendly platform name
        """
        platform_mapping = {
            "AWS": "AWS",
            "aws": "AWS",
            "databricks": "Databricks",
            "Databricks": "Databricks",
            "snowflakes": "Snowflakes",
            "Snowflakes": "Snowflakes",
            "google_cloud": "Google Cloud",
            "Google Cloud": "Google Cloud"
        }
        return platform_mapping.get(platform_type, platform_type or "Unknown")

    def get_top_recommendations(
        self,
        platform: str,
        limit: int = 6
    ) -> TopRecommendationResponse:
        """
        Get top recommendations based on potential savings.
        
        Args:
            platform: The platform filter (aws, databricks, snowflakes, google_cloud, all_platform)
            limit: Maximum number of recommendations to return (default: 6)
            
        Returns:
            TopRecommendationResponse with formatted recommendations
        """
        # Fetch recommendations from database
        recommendations = self.dao.get_top_recommendations(
            platform=platform,
            limit=limit
        )

        # Transform to response format
        recommendation_items: List[RecommendationItem] = []
        
        for rec in recommendations:
            item = RecommendationItem(
                platform_name=self._get_platform_display_name(rec.type),
                description=rec.description or rec.recommendation or "Recommended optimization",
                value=self._format_savings(rec.potential)
            )
            recommendation_items.append(item)

        # Build success response
        success_response = SuccessResponse(
            status_code=200,
            message="Data Received Successfully",
            status=True,
            data=recommendation_items
        )

        return TopRecommendationResponse(success_response=success_response)
