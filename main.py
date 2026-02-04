from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import auth, products, routines

app = FastAPI()

# --- 1. Подключение Роутеров (Backend API) ---
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(routines.router)


# --- 2. Настройка Frontend (HTML Templates) ---
templates = Jinja2Templates(directory="templates")




# Главная страница (Index)
@app.get("/", response_class=HTMLResponse)
async def page_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Страница регистрации
@app.get("/register_page", response_class=HTMLResponse)
async def page_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Страница входа
@app.get("/login_page", response_class=HTMLResponse)
async def page_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Страница каталога продуктов
@app.get("/products_page", response_class=HTMLResponse)
async def page_products(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

# Страница "Мои рутины" (Основная логика Студента 2)
@app.get("/routines_page", response_class=HTMLResponse)
async def page_routines(request: Request):
    return templates.TemplateResponse("routines.html", {"request": request})

# Страница аналитики (Агрегация Студента 2)
@app.get("/stats_page", response_class=HTMLResponse)
async def page_stats(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})