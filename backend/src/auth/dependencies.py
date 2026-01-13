"""
Authentication dependencies.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
import jwt
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        Decoded user information from token
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status_code": 401,
                    "error": "UNAUTHORIZED",
                    "message": "Authentication failed",
                    "details": "Invalid token payload"
                }
            )
            
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "roles": payload.get("roles", [])
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": 401,
                "error": "UNAUTHORIZED",
                "message": "Authentication failed",
                "details": "Token has expired"
            }
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": 401,
                "error": "UNAUTHORIZED",
                "message": "Authentication failed",
                "details": "Invalid token"
            }
        )
