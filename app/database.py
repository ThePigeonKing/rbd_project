from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Получение параметров подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
