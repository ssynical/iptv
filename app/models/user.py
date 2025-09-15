from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, EmailStr, Field
from .base import BaseModel

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_admin: bool = False
    max_connections: int = 1
    allowed_ips: List[str] = []
    expires_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
class UserCreate(PydanticBaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[EmailStr] = None
    max_connections: int = 1
    expires_at: Optional[datetime] = Field(default=None, description="account expiry date, null for no expiry")
    
class UserInDB(User):
    hashed_password: str