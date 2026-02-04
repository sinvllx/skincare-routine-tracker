# 🧴 Skincare Tracker

> A web application for managing skincare products and personal routines with brand analytics.

## 📋 Project Overview

**Skincare Tracker** is a full‑stack web app built with FastAPI and MongoDB that lets you:
- manage a skincare product catalog (CRUD)
- build personal routines (morning/evening, etc.)
- add or remove products from routine steps
- view analytics for the most popular brands
- use registration and login with JWT

**Technology Stack:**
- **Backend:** FastAPI (Python)
- **Database:** MongoDB (NoSQL)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Jinja2 templates
- **Authentication:** passlib (bcrypt), python-jose (JWT)
- **Async Driver:** Motor (AsyncIO MongoDB Driver)
- **Config:** python-dotenv

**Key Features:**
✅ RESTful API for products and routines  
✅ Embedded data model (products inside routines)  
✅ Advanced MongoDB updates ($push, $pull)  
✅ Aggregation pipeline for brand analytics  
✅ JWT authentication  
✅ Jinja2-based web pages


##  System Architecture

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Jinja2)                      │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐ │
│  │ index.html   │ register.html│ login.html   │ products  │ │
│  │ (Home)       │ (Register)   │ (Login)      │ (Catalog) │ │
│  └──────────────┴──────────────┴──────────────┴────────────┘ │
│  ┌──────────────┬──────────────┐                             │
│  │ routines.html│ stats.html   │                             │
│  │ (My Routines)│ (Analytics)  │                             │
│  └──────────────┴──────────────┘                             │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ENDPOINTS                                              │ │
│  │ • POST   /register (Register)                          │ │
│  │ • POST   /token (Login)                                │ │
│  │ • GET    /products (Read All)                          │ │
│  │ • GET    /products/{id} (Read One)                     │ │
│  │ • POST   /products (Create)                            │ │
│  │ • PUT    /products/{id} (Update)                       │ │
│  │ • DELETE /products/{id} (Delete)                       │ │
│  │ • POST   /routines (Create Routine)                    │ │
│  │ • GET    /routines/{user_email} (Read User Routines)   │ │
│  │ • PUT    /routines/{id}/add_step (Add Product)         │ │
│  │ • PUT    /routines/{id}/remove_step (Remove Product)   │ │
│  │ • GET    /stats/top_brands (Aggregation)               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                       ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ BUSINESS LOGIC & VALIDATION                             │ │
│  │ • Password hashing (bcrypt)                             │ │
│  │ • JWT tokens (python-jose)                              │ │
│  │ • Pydantic validation                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ TCP/27017
┌──────────────────────────▼──────────────────────────────────┐
│             MongoDB Database (skincare_db)                  │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ users        │ products     │ routines                 │
│  │ Collection   │ Collection   │ Collection               │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Registration/Login Flow**
   ```
   User Input → Validation (Pydantic) → Password Hashing (bcrypt) → MongoDB Storage → JWT
   ```

2. **Product Catalog Flow**
   ```
   Create Form → Product Schema → Validation → MongoDB Insert → Return with ID
   ```

3. **Routine Builder Flow**
   ```
   Add Step → $push Update → MongoDB → Response
   ```

4. **Analytics Flow**
   ```
   Stats Request → Aggregation Pipeline → Group/Sort/Limit → JSON Response
   ```


## 🗄️ Database Schema

### MongoDB Collections

#### **1. Products Collection**
```json
{
  "_id": ObjectId("..."),
  "name": "Niacinamide 10% + Zinc 1%",
  "brand": "The Ordinary",
  "category": "Serum",
  "price": 6.50
}
```

**Field Specifications:**
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `_id` | ObjectId | Unique identifier | Auto-generated |
| `name` | String | Product name | min_length: 2 |
| `brand` | String | Brand name | Required |
| `category` | String | Category | Required |
| `price` | Float | Price | > 0 |

#### **2. Users Collection**
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "password": "$2b$12$..."
}
```

**Field Specifications:**
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `_id` | ObjectId | Unique identifier | Auto-generated |
| `email` | String | User email | Valid email format |
| `password` | String | Hashed password | bcrypt hash |

#### **3. Routines Collection**
```json
{
  "_id": ObjectId("..."),
  "name": "Morning Routine",
  "user_email": "user@example.com",
  "products": [
    {
      "name": "Hydrating Cleanser",
      "brand": "CeraVe"
    }
  ]
}
```

**Field Specifications:**
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `_id` | ObjectId | Unique identifier | Auto-generated |
| `name` | String | Routine name | min_length: 1 |
| `user_email` | String | Owner email | Valid email format |
| `products` | Array | Embedded products | Optional |


## 🔍 MongoDB Queries

### 1. **Create Product**
```javascript
db.products.insertOne({
  name: "Niacinamide 10% + Zinc 1%",
  brand: "The Ordinary",
  category: "Serum",
  price: 6.50
})
```

### 2. **Get All Products**
```javascript
db.products.find({})
```

### 3. **Add Product to Routine ($push)**
```javascript
db.routines.updateOne(
  { "_id": ObjectId("64e5f8c9d4e2b9a1c3f4e5g6") },
  { "$push": { "products": { "name": "Hydrating Cleanser", "brand": "CeraVe" } } }
)
```

### 4. **Remove Product from Routine ($pull)**
```javascript
db.routines.updateOne(
  { "_id": ObjectId("64e5f8c9d4e2b9a1c3f4e5g6") },
  { "$pull": { "products": { "name": "Hydrating Cleanser" } } }
)
```

### 5. **Analytics - Top Brands (Aggregation Pipeline)**
```javascript
db.routines.aggregate([
  { "$unwind": "$products" },
  { "$group": { "_id": "$products.brand", "count": { "$sum": 1 } } },
  { "$sort": { "count": -1 } },
  { "$limit": 5 }
])
```


## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### 1. **User Registration**
```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Secret123"
}
```
**Response:** `200 OK`
```json
{
  "message": "User created successfully"
}
```

### 2. **User Login**
```http
POST /token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Secret123"
}
```
**Response:** `200 OK`
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### 3. **Create Product**
```http
POST /products
Content-Type: application/json

{
  "name": "Niacinamide 10% + Zinc 1%",
  "brand": "The Ordinary",
  "category": "Serum",
  "price": 6.50
}
```
**Response:** `200 OK`
```json
{
  "id": "...",
  "name": "Niacinamide 10% + Zinc 1%",
  "brand": "The Ordinary",
  "category": "Serum",
  "price": 6.5
}
```

### 4. **Get All Products**
```http
GET /products
```

### 5. **Update Product**
```http
PUT /products/{id}
Content-Type: application/json

{
  "price": 7.25
}
```
**Response:** `200 OK`
```json
{
  "message": "Product updated successfully"
}
```

### 6. **Delete Product**
```http
DELETE /products/{id}
```
**Response:** `200 OK`
```json
{
  "message": "Product deleted successfully"
}
```

### 7. **Create Routine**
```http
POST /routines
Content-Type: application/json

{
  "name": "Morning Routine",
  "user_email": "user@example.com"
}
```
**Response:** `200 OK`
```json
{
  "id": "..."
}
```

### 8. **Get User Routines**
```http
GET /routines/{user_email}
```

### 9. **Add Step to Routine**
```http
PUT /routines/{id}/add_step
Content-Type: application/json

{
  "name": "Hydrating Cleanser",
  "brand": "CeraVe"
}
```
**Response:** `200 OK`
```json
{
  "message": "Step added successfully"
}
```

### 10. **Remove Step from Routine**
```http
PUT /routines/{id}/remove_step
Content-Type: application/json

{
  "product_name": "Hydrating Cleanser"
}
```
**Response:** `200 OK`
```json
{
  "message": "Step removed successfully"
}
```

### 11. **Top Brands Analytics**
```http
GET /stats/top_brands
```


## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MongoDB 4.4+
- pip package manager

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create .env
# MONGO_URI=mongodb://localhost:27017
# SECRET_KEY=your_secret
# ALGORITHM=HS256

# Start MongoDB
mongod

# Run the application
uvicorn main:app --reload
```

### Access the Application
- **Frontend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)


## 📚 Project Files

```
skincare_tracker/
├── main.py                  # FastAPI app & routes
├── database.py              # MongoDB connection & helpers
├── models.py                # Pydantic models
├── routers/
│   ├── auth.py              # Register/Login (JWT)
│   ├── products.py          # Product CRUD
│   └── routines.py          # Routines + analytics
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── routines.html
│   └── stats.html
└── requirements.txt
```


## 🔐 Security Considerations

1. **Password Storage:** bcrypt hashing with automatic salt generation
2. **JWT:** short‑lived tokens (default 60 minutes)
3. **Input Validation:** Pydantic model validation
4. **Secrets:** use `.env` for `MONGO_URI`, `SECRET_KEY`, `ALGORITHM`


**Last Updated:** February 4, 2026
