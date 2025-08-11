"""
📋 Authentication schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str = Field(..., min_length=1, max_length=50, description="Username")
    password: str = Field(..., min_length=1, max_length=100, description="Password")

class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: "UserInfo"

class UserInfo(BaseModel):
    """User information schema"""
    username: str = Field(..., description="Username")
    role: str = Field(..., description="User role")
    permissions: List[str] = Field(..., description="User permissions")

class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None

# Update forward references
LoginResponse.model_rebuild()
