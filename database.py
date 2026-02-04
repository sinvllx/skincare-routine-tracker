import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db = client.skincare_db

user_collection = db.get_collection("users")
product_collection = db.get_collection("products")

routine_collection = db.get_collection("routines")



def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "brand": product["brand"],
        "category": product["category"],
        "price": product["price"],
    }

def routine_helper(routine) -> dict:
    return {
        "id": str(routine["_id"]),
        "name": routine["name"],
        "user_email": routine["user_email"],
        "products": routine.get("products", [])
    }