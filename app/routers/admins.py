from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Appointment, Animal, Clinic, OwnerAnimal
from app.schemas import AppointmentSchema, AnimalSchema
from app.database import get_db
from typing import List, Optional
from sqlalchemy.sql import text

router = APIRouter(
    prefix="/api/admins",
    tags=["admins"]
)

@router.get("/schedule/{branch_id}", response_model=List[AppointmentSchema])
def get_schedule(branch_id: int, db: Session = Depends(get_db)):
    """
    Получение расписания для указанного филиала.
    """
    appointments = db.query(Appointment).filter(Appointment.branch_id == branch_id).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this branch")
    return appointments


@router.get("/animal-card/{animal_id}", response_model=AnimalSchema)
def get_animal_card(animal_id: int, db: Session = Depends(get_db)):
    """
    Получение карточки животного по его ID.
    """
    animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.get("/history/{animal_id}", response_model=List[AppointmentSchema])
def get_appointment_history(animal_id: int, global_search: Optional[bool] = False, db: Session = Depends(get_db)):
    """
    Получение полной истории приёмов для указанного животного.
    Если global_search=True, делает запрос через dblink к центральной базе данных (main_office).
    """
    if global_search:
        try:
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
                raise HTTPException(status_code=404, detail="No appointment history found for this animal in main office")

            return [
                {
                    "appointment_id": row.appointment_id,
                    "animal_id": row.animal_id,
                    "employee_id": row.employee_id,
                    "branch_id": row.branch_id,
                    "appointment_date": row.appointment_date,
                    "appointment_time": row.appointment_time,
                    "complaints": row.complaints,
                    "diagnosis": row.diagnosis,
                    "treatment": row.treatment,
                    "notes": row.notes,
                    "cost": row.cost,
                    "payment_status": row.payment_status
                }
                for row in results
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying main office database: {str(e)}")

    # Локальный поиск
    appointments = db.query(Appointment).filter(Appointment.animal_id == animal_id).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointment history found for this animal")
    return appointments
