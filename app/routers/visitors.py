from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Appointment, Animal, Clinic, OwnerAnimal
from app.schemas import AppointmentSchema, AnimalSchema
from app.database import get_db
from typing import List
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/api/visitors",
    tags=["visitors"]
)

@router.get("/available-time/{branch_id}/{day}", response_model=List[str])
def get_available_time(branch_id: int, day: str, db: Session = Depends(get_db)):
    """
    Получение списка доступного времени для записи в указанном филиале и день.
    """
    try:
        appointment_date = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Клиника работает с 9:00 до 23:00
    opening_time = datetime.strptime("09:00", "%H:%M").time()
    closing_time = datetime.strptime("23:00", "%H:%M").time()

    # Запрос всех записей для указанного филиала и дня
    appointments = db.query(Appointment).filter(
        Appointment.source_branch == branch_id,
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
    available_slots = [slot.strftime("%H:%M") for slot in all_slots]

    return available_slots


@router.get("/animal-status/{animal_id}", response_model=AnimalSchema)
def get_animal_status(animal_id: int, db: Session = Depends(get_db)):
    """
    Получение статуса животного по его ID.
    """
    animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.post("/book-appointment", response_model=AppointmentSchema)
def book_appointment(appointment: AppointmentSchema, db: Session = Depends(get_db)):
    """
    Запись на приём в клинику.
    """
    new_appointment = Appointment(
        animal_id=appointment.animal_id,
        employee_id=appointment.employee_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        complaints=appointment.complaints,
        diagnosis=appointment.diagnosis,
        treatment=appointment.treatment,
        notes=appointment.notes,
        cost=appointment.cost,
        payment_status=appointment.payment_status,
        branch_id=appointment.branch_id
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
