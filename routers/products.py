from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from database import product_collection, product_helper
from models import ProductSchema

router = APIRouter(tags=["Products"])

# 1. READ ALL (Получить список всех продуктов)
@router.get("/products")
async def get_all_products():
    """
    Возвращает список всей косметики из базы данных.
    """
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products

@router.get("/products/{id}")
async def get_product(id: str):
    """
    Ищет конкретный продукт по его MongoDB ObjectId.
    """
    # Проверяем валидность ID
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)
    
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/products")
async def create_product(product: ProductSchema):
    """
    Добавляет новый продукт в базу.
    Данные валидируются через Pydantic (ProductSchema).
    """
    product_dict = product.dict()
    
    new_product = await product_collection.insert_one(product_dict)
    
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    return product_helper(created_product)

# 4. UPDATE (Обновить продукт - Basic Update)
@router.put("/products/{id}")
async def update_product(id: str, data: dict = Body(...)):
    """
    Обновляет поля продукта.
    Использует оператор $set для частичного обновления.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    data = {k: v for k, v in data.items() if v is not None}

    if len(data) >= 1:
        update_result = await product_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": data}
        )

        if update_result.modified_count == 1:
            return {"message": "Product updated successfully"}

    existing_product = await product_collection.find_one({"_id": ObjectId(id)})
    if existing_product:
        return {"message": "No changes made or data is same"}
    
    raise HTTPException(status_code=404, detail="Product not found")

# 5. DELETE (Удалить продукт)
@router.delete("/products/{id}")
async def delete_product(id: str):
    """
    Удаляет продукт из базы данных навсегда.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    delete_result = await product_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return {"message": "Product deleted successfully"}

    raise HTTPException(status_code=404, detail="Product not found")