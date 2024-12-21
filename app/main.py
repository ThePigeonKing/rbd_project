from fastapi import FastAPI
from app.routers import visitors, admins
from app.database import Base, engine

# Создание таблиц при запуске приложения
# Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI(title="Vet Clinic API", version="1.0")

# Подключение роутеров
app.include_router(visitors.router)
app.include_router(admins.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Vet Clinic API"}
