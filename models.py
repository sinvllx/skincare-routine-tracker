from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserSchema(BaseModel):
    """Модель для регистрации пользователя"""
    email: EmailStr
    password: str = Field(..., min_length=4)

class UserLogin(BaseModel):
    """Модель для входа в систему"""
    email: EmailStr
    password: str

class ProductSchema(BaseModel):
    """Модель для создания нового продукта"""
    name: str = Field(..., min_length=2, description="Название продукта")
    brand: str = Field(..., description="Бренд производителя")
    category: str = Field(..., description="Категория (например, Serum, Toner)")
    price: float = Field(..., gt=0, description="Цена должна быть больше 0")

    class Config:
        schema_extra = {
            "example": {
                "name": "Niacinamide 10% + Zinc 1%",
                "brand": "The Ordinary",
                "category": "Serum",
                "price": 6.50
            }
        }

class ProductUpdate(BaseModel):
    """Модель для обновления продукта (все поля опциональны)"""
    name: Optional[str]
    brand: Optional[str]
    category: Optional[str]
    price: Optional[float]



class RoutineCreate(BaseModel):
    """Модель для создания пустой рутины"""
    name: str = Field(..., min_length=1, description="Название рутины (Утро, Вечер)")
    user_email: EmailStr

class ProductEmbedded(BaseModel):
    """
    Модель продукта, который встраивается (embed) внутрь рутины.
    Это нужно для реализации Embedded Data Model.
    """
    name: str
    brand: str