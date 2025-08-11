"""
🔐 Authentication routes for admin access
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional, List

from ....core.config import settings
from ....core.logger import api_logger

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security scheme
security = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "allerscan_secret_key_2024_svm_adaboost"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Admin credentials (hashed passwords)
ADMIN_CREDENTIALS = {
    "admin": {
        "username": "admin",
        "password_hash": "$2b$12$6sQ1qEIfpV6ZVrXtFSyZK.ucVxgHjHClSj.9yZ69209By4GavObN.",  # admin123
        "role": "admin",
        "permissions": ["view_dataset", "download_data", "manage_system"]
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate user credentials"""
    user = ADMIN_CREDENTIALS.get(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user still exists
        if username not in ADMIN_CREDENTIALS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return ADMIN_CREDENTIALS[username]
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_admin(current_user: dict = Depends(verify_token)):
    """Require admin role"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    🔐 Admin login endpoint
    
    Authenticate admin user and return JWT token.
    Default credentials: username=admin, password=admin123
    """
    try:
        # Authenticate user
        user = authenticate_user(request.username, request.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"], "role": user["role"]}, 
            expires_delta=access_token_expires
        )
        
        api_logger.info(f"Admin login successful: {user['username']}")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "username": user["username"],
                "role": user["role"],
                "permissions": user["permissions"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/verify")
async def verify_admin_token(current_user: dict = Depends(verify_token)):
    """
    Verify admin token
    """
    return {
        "success": True,
        "username": current_user["username"],
        "role": current_user["role"],
        "permissions": current_user["permissions"],
        "message": "Token is valid"
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(verify_token)):
    """
    Admin logout (client should discard token)
    """
    api_logger.info(f"Admin logout: {current_user['username']}")
    return {
        "success": True,
        "message": "Logout successful"
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(verify_token)):
    """
    Get current user information
    """
    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "permissions": current_user["permissions"]
    }

# Export
__all__ = ["router", "require_admin"]
