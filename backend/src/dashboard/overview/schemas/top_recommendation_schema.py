"""
Pydantic schemas for Top Recommendations API.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# Request Schema
class TopRecommendationRequest(BaseModel):
    """Request schema for top recommendations endpoint."""
    platform: Literal["all_platform", "google_cloud", "aws", "databricks", "snowflakes"] = Field(
        ...,
        description="Platform filter for recommendations"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "platform": "aws"
            }
        }


# Response Data Schema
class RecommendationItem(BaseModel):
    """Single recommendation item in response."""
    platform_name: str = Field(..., description="Name of the platform (AWS, Databricks, Snowflakes)")
    description: str = Field(..., description="Recommendation description")
    value: str = Field(..., description="Potential savings value formatted as 'Save $XXX.XX'")

    class Config:
        json_schema_extra = {
            "example": {
                "platform_name": "AWS",
                "description": "Recommended to right-size EC2 instance",
                "value": "Save $781.12"
            }
        }


class SuccessResponse(BaseModel):
    """Success response wrapper."""
    status_code: int = Field(default=200, description="HTTP status code")
    message: str = Field(default="Data Received Successfully", description="Response message")
    status: bool = Field(default=True, description="Success status")
    data: List[RecommendationItem] = Field(default=[], description="List of recommendations")


class TopRecommendationResponse(BaseModel):
    """Full response schema for top recommendations."""
    success_response: SuccessResponse

    class Config:
        json_schema_extra = {
            "example": {
                "success_response": {
                    "status_code": 200,
                    "message": "Data Received Successfully",
                    "status": True,
                    "data": [
                        {
                            "platform_name": "AWS",
                            "description": "Recommended to right-size EC2 instance",
                            "value": "Save $781.12"
                        }
                    ]
                }
            }
        }


# Error Response Schemas
class ErrorDetail(BaseModel):
    """Error detail schema."""
    status_code: int
    error: str
    message: str
    details: Optional[str] = None
    retry_after_seconds: Optional[int] = None


class InvalidRequestError(ErrorDetail):
    """400 Bad Request error."""
    status_code: int = 400
    error: str = "INVALID_REQUEST"
    message: str = "Invalid request parameters"
    details: dict = {}


class UnauthorizedError(ErrorDetail):
    """401 Unauthorized error."""
    status_code: int = 401
    error: str = "UNAUTHORIZED"
    message: str = "Authentication failed"
    details: str = "Invalid email or password"


class ForbiddenError(ErrorDetail):
    """403 Forbidden error."""
    status_code: int = 403
    error: str = "FORBIDDEN"
    message: str = "Account locked"
    details: str = "Too many failed login attempts. Please try again after 15 minutes."


class NotFoundError(ErrorDetail):
    """404 Not Found error."""
    status_code: int = 404
    error: str = "NOT_FOUND"
    message: str = "User not found"
    details: str = "No account exists with the provided email"


class TooManyRequestsError(ErrorDetail):
    """429 Too Many Requests error."""
    status_code: int = 429
    error: str = "TOO_MANY_REQUESTS"
    message: str = "Too many login attempts"
    retry_after_seconds: int = 300


class InternalServerError(ErrorDetail):
    """500 Internal Server Error."""
    status_code: int = 500
    error: str = "INTERNAL_SERVER_ERROR"
    message: str = "An unexpected error occurred"
    details: str = "Please try again later or contact support"


class ServiceUnavailableError(ErrorDetail):
    """503 Service Unavailable error."""
    status_code: int = 503
    error: str = "SERVICE_UNAVAILABLE"
    message: str = "Service temporarily unavailable"
    retry_after_seconds: int = 60
