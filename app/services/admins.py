# services/admins.py

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models import Appointment, Animal
from typing import List

def get_schedule(branch_id: int, db: Session) -> List[Appointment]:
    """
    Возвращает расписание для указанного филиала.
    """
    appointments = db.query(Appointment).filter(Appointment.branch_id == branch_id).all()
    return appointments


def get_animal_card(animal_id: int, db: Session) -> Animal:
    """
    Возвращает карточку животного по его ID.
    """
    animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not animal:
        raise ValueError("Animal not found")
    return animal


def get_appointment_history(animal_id: int, global_search: bool, db: Session) -> List[Appointment]:
    """
    Возвращает историю приёмов для указанного животного.
    Если global_search=True, выполняется запрос в главную базу данных (main_office).
    """
    if global_search:
        query = text(
            """
            SELECT * FROM dblink('dbname=main_office_db user=main_office_user password=main_office_password',
                                 'SELECT * FROM appointment WHERE animal_id = :animal_id')
            AS t(appointment_id INTEGER, animal_id INTEGER, employee_id INTEGER, branch_id INTEGER, 
                 appointment_date DATE, appointment_time TIME, complaints TEXT, diagnosis TEXT, 
                 treatment TEXT, notes TEXT, cost DECIMAL, payment_status VARCHAR);
            """
        )
        results = db.execute(query, {"animal_id": animal_id}).fetchall()
        if not results:
            raise ValueError("No appointment history found for this animal in main office")
        
        return [
            Appointment(
                appointment_id=row.appointment_id,
                animal_id=row.animal_id,
                employee_id=row.employee_id,
                branch_id=row.branch_id,
                appointment_date=row.appointment_date,
                appointment_time=row.appointment_time,
                complaints=row.complaints,
                diagnosis=row.diagnosis,
                treatment=row.treatment,
                notes=row.notes,
                cost=row.cost,
                payment_status=row.payment_status
            ) for row in results
        ]

    # Локальный поиск
    appointments = db.query(Appointment).filter(Appointment.animal_id == animal_id).all()
    if not appointments:
        raise ValueError("No appointment history found for this animal")
    return appointments
