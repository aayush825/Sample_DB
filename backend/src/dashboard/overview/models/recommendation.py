"""
Database model for AWS Recommendation Consolidate table.
"""
from sqlalchemy import Column, BigInteger, Text, Numeric, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from src.database.base import Base


class AWSRecommendationConsolidate(Base):
    """Model for aws_recommendation_consolidate table."""
    
    __tablename__ = "aws_recommendation_consolidate"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(Text, nullable=True)
    account = Column(Text, nullable=True)
    region = Column(Text, nullable=True)
    resource_name = Column(Text, nullable=True)
    resource_id = Column(Text, nullable=True)
    service = Column(Text, nullable=True)
    sub_service = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    potential = Column(Numeric(18, 4), nullable=True)
    actual_cost = Column(Numeric(18, 4), nullable=True)
    target_cost = Column(Numeric(18, 4), nullable=True)
    current_configuration = Column(Text, nullable=True)
    expected_configuration = Column(Text, nullable=True)
    justifications = Column(Text, nullable=True)
    tags_json = Column(JSONB, nullable=True)
    actionable = Column(Boolean, nullable=True)
    risk_level = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)

    def __repr__(self):
        return f"<AWSRecommendationConsolidate(id={self.id}, resource_name={self.resource_name})>"
