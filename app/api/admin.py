from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.auth import get_current_user
from app.models.user import UserInDB
from app.models.category import Category, CategoryCreate
from app.models.stream import Stream, StreamCreate
from app.models.subscription import Subscription, SubscriptionCreate
from app.database import get_database
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])

async def require_admin(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin access required"
        )
    return current_user

@router.post("/categories", response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    admin_user: UserInDB = Depends(require_admin)
):
    db = get_database()
    
    existing = await db.categories.find_one({"category_id": category_data.category_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="category id already exists"
        )
    
    category_dict = category_data.model_dump()
    category_dict["created_at"] = datetime.utcnow()
    category_dict["updated_at"] = datetime.utcnow()
    
    category = Category(**category_dict)
    result = await db.categories.insert_one(category.model_dump(by_alias=True))
    
    created_category = await db.categories.find_one({"_id": result.inserted_id})
    return Category(**created_category)

@router.get("/categories", response_model=List[Category])
async def list_categories(admin_user: UserInDB = Depends(require_admin)):
    db = get_database()
    categories = await db.categories.find().sort("sort_order", 1).to_list(None)
    return [Category(**cat) for cat in categories]

@router.post("/streams", response_model=Stream)
async def create_stream(
    stream_data: StreamCreate,
    admin_user: UserInDB = Depends(require_admin)
):
    db = get_database()
    
    existing = await db.streams.find_one({"stream_id": stream_data.stream_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="stream id already exists"
        )
    
    stream_dict = stream_data.model_dump()
    stream_dict["created_at"] = datetime.utcnow()
    stream_dict["updated_at"] = datetime.utcnow()
    if not stream_dict.get("added"):
        stream_dict["added"] = str(int(datetime.utcnow().timestamp()))
    
    # convert any url objects to strings before saving to mongodb
    if stream_dict.get("stream_icon"):
        stream_dict["stream_icon"] = str(stream_dict["stream_icon"])
    if stream_dict.get("direct_source"):
        stream_dict["direct_source"] = str(stream_dict["direct_source"])
    
    result = await db.streams.insert_one(stream_dict)
    
    created_stream = await db.streams.find_one({"_id": result.inserted_id})
    return Stream(**created_stream)

@router.get("/streams", response_model=List[Stream])
async def list_streams(
    stream_type: str = None,
    admin_user: UserInDB = Depends(require_admin)
):
    db = get_database()
    query = {}
    if stream_type:
        query["stream_type"] = stream_type
    
    streams = await db.streams.find(query).to_list(None)
    return [Stream(**stream) for stream in streams]

@router.post("/subscriptions", response_model=Subscription)
async def create_subscription(
    sub_data: SubscriptionCreate,
    admin_user: UserInDB = Depends(require_admin)
):
    db = get_database()
    
    existing = await db.subscriptions.find_one({"username": sub_data.username})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="subscription username already exists"
        )
    
    sub_dict = sub_data.model_dump()
    sub_dict["created_at"] = datetime.utcnow()
    sub_dict["updated_at"] = datetime.utcnow()
    
    subscription = Subscription(**sub_dict)
    result = await db.subscriptions.insert_one(subscription.model_dump(by_alias=True))
    
    created_sub = await db.subscriptions.find_one({"_id": result.inserted_id})
    return Subscription(**created_sub)

@router.get("/subscriptions", response_model=List[Subscription])
async def list_subscriptions(admin_user: UserInDB = Depends(require_admin)):
    db = get_database()
    subs = await db.subscriptions.find().to_list(None)
    return [Subscription(**sub) for sub in subs]