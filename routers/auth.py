from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from database import user_collection
from models import UserSchema, UserLogin

# Создаем роутер
router = APIRouter(tags=["Auth"])

# --- Настройки Безопасности ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_fallback")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password, hashed_password):
    """Проверяет, совпадает ли введенный пароль с хешем в БД"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Хеширует пароль перед сохранением"""
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """Генерирует JWT токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Эндпоинты (API) ---

@router.post("/register")
async def register(user: UserSchema):
    """
    Регистрация нового пользователя.
    1. Проверяет, есть ли такой email.
    2. Хеширует пароль.
    3. Сохраняет в MongoDB.
    """
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = {
        "email": user.email,
        "password": hashed_password
    }
    await user_collection.insert_one(new_user)
    
    return {"message": "User created successfully"}

@router.post("/token")
async def login(user: UserLogin):
    """
    Вход в систему (Login).
    1. Ищет пользователя по email.
    2. Проверяет пароль.
    3. Если всё ок, выдает JWT токен.
    """
    db_user = await user_collection.find_one({"email": user.email})
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}