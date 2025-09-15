from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Optional, List, Dict, Any
from app.database import get_database
from app.models.subscription import Subscription
from app.models.category import Category
from app.models.stream import Stream
from datetime import datetime
import json

router = APIRouter(tags=["xtream"])

async def authenticate_xtream_user(username: str, password: str) -> Optional[Subscription]:
    db = get_database()
    sub_data = await db.subscriptions.find_one({"username": username, "password": password})
    if not sub_data:
        return None
    
    subscription = Subscription(**sub_data)
    
    if subscription.exp_date and subscription.exp_date < datetime.utcnow():
        return None
    
    return subscription

async def require_xtream_auth(
    username: str = Query(...),
    password: str = Query(...)
) -> Subscription:
    subscription = await authenticate_xtream_user(username, password)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )
    return subscription

@router.get("/player_api.php")
async def player_api(
    action: str = Query(...),
    username: str = Query(...),
    password: str = Query(...),
    category_id: Optional[str] = Query(None)
):
    subscription = await authenticate_xtream_user(username, password)
    if not subscription:
        return {"user_info": {"auth": 0, "status": "Disabled", "message": "invalid credentials"}}
    
    if action == "get_live_categories":
        return await get_live_categories(subscription)
    elif action == "get_vod_categories":
        return await get_vod_categories(subscription)
    elif action == "get_series_categories":
        return await get_series_categories(subscription)
    elif action == "get_live_streams":
        return await get_live_streams(subscription, category_id)
    elif action == "get_vod_streams":
        return await get_vod_streams(subscription, category_id)
    elif action == "get_series":
        return await get_series(subscription, category_id)
    else:
        raise HTTPException(status_code=400, detail="invalid action")

async def get_live_categories(subscription: Subscription) -> List[Dict[str, Any]]:
    db = get_database()
    categories = await db.categories.find({"parent_id": {"$in": [None, ""]}}).sort("sort_order", 1).to_list(None)
    
    result = []
    for cat in categories:
        category = Category(**cat)
        result.append({
            "category_id": category.category_id,
            "category_name": category.category_name,
            "parent_id": 0
        })
    
    return result

async def get_vod_categories(subscription: Subscription) -> List[Dict[str, Any]]:
    db = get_database()
    categories = await db.categories.find({"parent_id": {"$in": [None, ""]}}).sort("sort_order", 1).to_list(None)
    
    result = []
    for cat in categories:
        category = Category(**cat)
        result.append({
            "category_id": category.category_id,
            "category_name": category.category_name,
            "parent_id": 0
        })
    
    return result

async def get_series_categories(subscription: Subscription) -> List[Dict[str, Any]]:
    db = get_database()
    categories = await db.categories.find({"parent_id": {"$in": [None, ""]}}).sort("sort_order", 1).to_list(None)
    
    result = []
    for cat in categories:
        category = Category(**cat)
        result.append({
            "category_id": category.category_id,
            "category_name": category.category_name,
            "parent_id": 0
        })
    
    return result

async def get_live_streams(subscription: Subscription, category_id: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_database()
    
    query = {"stream_type": "live"}
    if category_id:
        query["category_id"] = category_id
    
    streams = await db.streams.find(query).to_list(None)
    
    result = []
    for stream_data in streams:
        stream = Stream(**stream_data)
        result.append({
            "num": stream.stream_id,
            "name": stream.name,
            "stream_type": "live",
            "stream_id": stream.stream_id,
            "stream_icon": str(stream.stream_icon) if stream.stream_icon else "",
            "epg_channel_id": stream.epg_channel_id or "",
            "added": stream.added or "",
            "category_id": stream.category_id,
            "custom_sid": stream.custom_sid or "",
            "tv_archive": stream.tv_archive,
            "direct_source": str(stream.direct_source) if stream.direct_source else "",
            "tv_archive_duration": stream.tv_archive_duration
        })
    
    return result

async def get_vod_streams(subscription: Subscription, category_id: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_database()
    
    query = {"stream_type": "movie"}
    if category_id:
        query["category_id"] = category_id
    
    streams = await db.streams.find(query).to_list(None)
    
    result = []
    for stream_data in streams:
        stream = Stream(**stream_data)
        result.append({
            "num": stream.stream_id,
            "name": stream.name,
            "stream_type": "movie",
            "stream_id": stream.stream_id,
            "stream_icon": str(stream.stream_icon) if stream.stream_icon else "",
            "added": stream.added or "",
            "category_id": stream.category_id,
            "container_extension": getattr(stream, 'container_extension', 'mp4'),
            "custom_sid": stream.custom_sid or "",
            "direct_source": str(stream.direct_source) if stream.direct_source else ""
        })
    
    return result

async def get_series(subscription: Subscription, category_id: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_database()
    
    query = {"stream_type": "series"}
    if category_id:
        query["category_id"] = category_id
    
    streams = await db.streams.find(query).to_list(None)
    
    result = []
    for stream_data in streams:
        stream = Stream(**stream_data)
        result.append({
            "num": stream.stream_id,
            "name": stream.name,
            "stream_type": "series",
            "series_id": stream.stream_id,
            "cover": stream.stream_icon or "",
            "plot": "",
            "cast": "",
            "director": "",
            "genre": "",
            "release_date": "",
            "last_modified": stream.added or "",
            "rating": "0",
            "rating_5based": 0,
            "backdrop_path": [],
            "youtube_trailer": "",
            "episode_run_time": "45",
            "category_id": stream.category_id
        })
    
    return result