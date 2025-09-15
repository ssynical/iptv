from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, Field
from .base import BaseModel

class Category(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=100)
    category_id: str = Field(..., min_length=1)
    parent_id: Optional[str] = None
    sort_order: int = 0
    
class CategoryCreate(PydanticBaseModel):
    category_name: str = Field(..., min_length=1, max_length=100)
    category_id: str = Field(..., min_length=1)
    parent_id: Optional[str] = None
    sort_order: int = 0