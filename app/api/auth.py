from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from app.core.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from app.core.exceptions import UserExistsError, UserNotFoundError
from app.models.user import User, UserCreate, UserInDB
from app.database import get_database
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBasic()

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    user = await authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="account is disabled"
        )
    
    if user.expires_at and user.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="account has expired"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    db = get_database()
    await db.users.update_one(
        {"username": user.username},
        {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400
    }

@router.post("/register", response_model=User)
async def register(user_data: UserCreate):
    db = get_database()
    
    existing_user = await db.users.find_one({"username": user_data.username})
    if existing_user:
        existing_user_obj = UserInDB(**existing_user)
        if existing_user_obj.expires_at and existing_user_obj.expires_at < datetime.utcnow():
            await db.users.delete_one({"username": user_data.username})
        else:
            raise UserExistsError("username already taken")
    
    if user_data.email:
        existing_email = await db.users.find_one({"email": user_data.email})
        if existing_email:
            existing_email_obj = UserInDB(**existing_email)
            if existing_email_obj.expires_at and existing_email_obj.expires_at < datetime.utcnow():
                await db.users.delete_one({"email": user_data.email})
            else:
                raise UserExistsError("email already registered")
    
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict["hashed_password"] = hashed_password
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    
    user_in_db = UserInDB(**user_dict)
    result = await db.users.insert_one(user_in_db.model_dump(by_alias=True))
    
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return User(**created_user)

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: UserInDB = Depends(get_current_user)):
    return User(**current_user.model_dump())

@router.delete("/users/{username}")
async def delete_user(username: str, current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin access required"
        )
    
    db = get_database()
    result = await db.users.delete_one({"username": username})
    
    if result.deleted_count == 0:
        raise UserNotFoundError("user not found")
    
    return {"message": f"user {username} deleted successfully"}

@router.post("/promote-admin/{username}")
async def promote_to_admin(username: str):
    db = get_database()
    result = await db.users.update_one(
        {"username": username},
        {"$set": {"is_admin": True, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise UserNotFoundError("user not found")
    
    return {"message": f"user {username} promoted to admin"}