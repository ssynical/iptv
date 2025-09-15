from typing import Optional, List, Dict, Any
from pydantic import BaseModel as PydanticBaseModel, Field, HttpUrl
from .base import BaseModel

class Stream(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    stream_type: str = Field(..., pattern="^(live|movie|series)$")
    stream_id: int = Field(..., gt=0)
    stream_icon: Optional[HttpUrl] = None
    epg_channel_id: Optional[str] = None
    added: Optional[str] = None
    category_id: str = Field(..., min_length=1)
    custom_sid: Optional[str] = None
    tv_archive: int = 0
    direct_source: Optional[HttpUrl] = None
    tv_archive_duration: int = 0
    
class LiveStream(Stream):
    stream_type: str = "live"
    
class MovieStream(Stream):
    stream_type: str = "movie"
    container_extension: str = Field(default="mp4")
    
class SeriesStream(Stream):
    stream_type: str = "series"
    
class StreamCreate(PydanticBaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    stream_type: str = Field(..., pattern="^(live|movie|series)$")
    stream_id: int = Field(..., gt=0)
    stream_icon: Optional[HttpUrl] = None
    epg_channel_id: Optional[str] = None
    added: Optional[str] = None
    category_id: str = Field(..., min_length=1)
    custom_sid: Optional[str] = None
    tv_archive: int = 0
    direct_source: Optional[HttpUrl] = None
    tv_archive_duration: int = 0
    container_extension: str = Field(default="mp4")