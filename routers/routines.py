from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from database import routine_collection, routine_helper
from models import RoutineCreate, ProductEmbedded

router = APIRouter(tags=["Routines"])

# 1. CREATE ROUTINE (Создать новую рутину)
@router.post("/routines")
async def create_routine(routine: RoutineCreate):
    """
    Создает "контейнер" для рутины (например, 'Утренний уход').
    Изначально список продуктов пуст.
    """
    routine_dict = routine.dict()
    routine_dict["products"] = []
    
    new_routine = await routine_collection.insert_one(routine_dict)
    return {"id": str(new_routine.inserted_id)}

# 2. GET USER ROUTINES (Получить рутины пользователя)
@router.get("/routines/{user_email}")
async def get_routines(user_email: str):
    """
    Находит все рутины, принадлежащие конкретному email.
    """
    routines = []
    async for r in routine_collection.find({"user_email": user_email}):
        routines.append(routine_helper(r))
    return routines

# 3. ADVANCED UPDATE: $push (Добавить шаг в рутину)
@router.put("/routines/{id}/add_step")
async def add_step(id: str, product: ProductEmbedded):
    """
    Добавляет продукт внутрь массива 'products' существующей рутины.
    Использует оператор $push (атомарное добавление).
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    result = await routine_collection.update_one(
        {"_id": ObjectId(id)},
        {"$push": {"products": product.dict()}} 
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Routine not found")
        
    return {"message": "Step added successfully"}

# 4. ADVANCED UPDATE: $pull (Удалить шаг из рутины)
@router.put("/routines/{id}/remove_step")
async def remove_step(id: str, product_name: str = Body(..., embed=True)):
    """
    Удаляет продукт из массива 'products' по названию.
    Использует оператор $pull (удаление по критерию).
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    result = await routine_collection.update_one(
        {"_id": ObjectId(id)},
        {"$pull": {"products": {"name": product_name}}}
    )
    
    if result.modified_count == 0:
        # Либо рутина не найдена, либо такого продукта там не было
        return {"message": "Routine not found or product not in list"}
        
    return {"message": "Step removed successfully"}

# 5. AGGREGATION PIPELINE (Аналитика для Dashboard)
@router.get("/stats/top_brands")
async def get_brand_stats():
    pipeline = [
        # Разворачивает массивы products. Если в рутине 3 продукта, станет 3 документа.
        {"$unwind": "$products"}, 
        
        # Группируем по названию бренда и считаем количество ($sum)
        {"$group": { 
            "_id": "$products.brand", 
            "count": {"$sum": 1}
        }},
        
        # Сортируем по убыванию количества (от популярного к редкому)
        {"$sort": {"count": -1}},  
        
        # Stage 4: $limit
        {"$limit": 5}              
    ]
    
    stats = await routine_collection.aggregate(pipeline).to_list(length=5)
    return stats