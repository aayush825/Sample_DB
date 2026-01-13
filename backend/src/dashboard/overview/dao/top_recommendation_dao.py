"""
Data Access Object for Top Recommendations.
Handles database queries for fetching top recommendations based on potential savings.
"""
from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from src.dashboard.overview.models.recommendation import AWSRecommendationConsolidate


class TopRecommendationDAO:
    """DAO class for Top Recommendation operations."""

    def __init__(self, db: Session):
        """Initialize the DAO with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_top_recommendations(
        self,
        platform: str,
        limit: int = 6
    ) -> List[AWSRecommendationConsolidate]:
        """
        Fetch top recommendations based on potential savings (actual_cost - target_cost).
        
        Args:
            platform: The platform filter (aws, databricks, snowflakes, google_cloud, all_platform)
            limit: Maximum number of recommendations to return (default: 6)
            
        Returns:
            List of top recommendations ordered by potential savings descending
        """
        query = self.db.query(AWSRecommendationConsolidate)
        
        # Apply platform filter if not 'all_platform'
        if platform and platform.lower() != "all_platform":
            # Map platform key to the type field in database
            platform_mapping = {
                "aws": "AWS",
                "databricks": "Databricks",
                "snowflakes": "Snowflakes",
                "google_cloud": "Google Cloud"
            }
            platform_type = platform_mapping.get(platform.lower())
            if platform_type:
                query = query.filter(
                    AWSRecommendationConsolidate.type == platform_type
                )
        
        # Filter for records with valid potential savings
        query = query.filter(
            AWSRecommendationConsolidate.potential.isnot(None),
            AWSRecommendationConsolidate.potential > 0
        )
        
        # Order by potential savings (descending) and limit results
        recommendations = (
            query
            .order_by(desc(AWSRecommendationConsolidate.potential))
            .limit(limit)
            .all()
        )
        
        return recommendations

    def get_recommendation_by_id(
        self,
        recommendation_id: int
    ) -> Optional[AWSRecommendationConsolidate]:
        """
        Fetch a single recommendation by ID.
        
        Args:
            recommendation_id: The ID of the recommendation
            
        Returns:
            The recommendation if found, None otherwise
        """
        return (
            self.db.query(AWSRecommendationConsolidate)
            .filter(AWSRecommendationConsolidate.id == recommendation_id)
            .first()
        )
