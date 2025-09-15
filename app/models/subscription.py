from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field
from .base import BaseModel

class Subscription(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=50)
    exp_date: Optional[datetime] = None
    max_connections: int = Field(default=1, ge=1, le=10)
    is_trial: bool = False
    active_cons: int = 0
    created_by: Optional[str] = None
    is_restreamer: bool = False
    bouquet: List[str] = []
    allowed_ips: List[str] = []
    allowed_ua: List[str] = []
    
class SubscriptionCreate(PydanticBaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=50)
    exp_date: Optional[datetime] = None
    max_connections: int = Field(default=1, ge=1, le=10)
    is_trial: bool = False
    created_by: Optional[str] = None
    is_restreamer: bool = False
    bouquet: List[str] = []
    allowed_ips: List[str] = []
    allowed_ua: List[str] = []