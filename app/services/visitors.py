# services/visitors.py

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models import Appointment, Animal
from typing import List
from datetime import datetime, timedelta

# 1. Получение доступного времени для записи в филиале

def get_available_time(branch_id: int, day: str, db: Session) -> List[str]:
    """
    Возвращает список доступного времени для записи в указанном филиале на заданный день.
    """
    try:
        appointment_date = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    # Клиника работает с 9:00 до 23:00
    opening_time = datetime.strptime("09:00", "%H:%M").time()
    closing_time = datetime.strptime("23:00", "%H:%M").time()

    # Запрос всех записей для указанного филиала и дня
    appointments = db.query(Appointment).filter(
        Appointment.branch_id == branch_id,
        Appointment.appointment_date == appointment_date
    ).all()

    # Генерация всех возможных слотов времени
    current_time = datetime.combine(appointment_date, opening_time)
    end_time = datetime.combine(appointment_date, closing_time)
    all_slots = []

    while current_time < end_time:
        all_slots.append(current_time.time())
        current_time += timedelta(minutes=30)

    # Удаление занятых слотов
    for appointment in appointments:
        start_time = appointment.appointment_time
        end_time = (datetime.combine(appointment_date, start_time) + timedelta(minutes=30)).time()
        all_slots = [slot for slot in all_slots if not (start_time <= slot < end_time)]

    # Преобразование оставшихся слотов в строки
    return [slot.strftime("%H:%M") for slot in all_slots]

# 2. Получение статуса животного

def get_animal_status(animal_id: int, db: Session) -> Animal:
    """
    Возвращает информацию о животном по его ID.
    """
    animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not animal:
        raise ValueError("Animal not found")
    return animal

# 3. Запись на приём

def book_appointment(data: dict, db: Session) -> Appointment:
    """
    Создаёт новую запись на приём в клинику.
    """
    new_appointment = Appointment(
        animal_id=data["animal_id"],
        employee_id=data["employee_id"],
        appointment_date=data["appointment_date"],
        appointment_time=data["appointment_time"],
        complaints=data.get("complaints"),
        diagnosis=data.get("diagnosis"),
        treatment=data.get("treatment"),
        notes=data.get("notes"),
        cost=data.get("cost"),
        payment_status=data.get("payment_status"),
        branch_id=data["branch_id"]
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
