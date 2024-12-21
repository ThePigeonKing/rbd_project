from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time

class PositionSchema(BaseModel):
    position_id: Optional[int]
    title: str
    description: Optional[str]
    medical_services: bool

    class Config:
        orm_mode = True


class ClinicSchema(BaseModel):
    clinic_id: Optional[int]
    name: str
    address: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class EmployeeSchema(BaseModel):
    employee_id: Optional[int]
    first_name: str
    last_name: str
    phone: str
    email: str
    position_id: Optional[int]
    clinic_id: Optional[int]

    class Config:
        orm_mode = True


class OwnerAnimalSchema(BaseModel):
    owner_id: Optional[int]
    first_name: str
    last_name: str
    address: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class AnimalSchema(BaseModel):
    animal_id: int
    name: str
    species: str
    breed: str
    date_of_birth: datetime
    gender: str
    owner_id: Optional[int]
    diabetes: Optional[bool]
    chronic_diseases: Optional[str]
    vaccinations: Optional[str]

    class Config:
        orm_mode = True



class AppointmentSchema(BaseModel):
    animal_id: int
    employee_id: int
    appointment_date: date  # Изменено на datetime.date
    appointment_time: time  # Изменено на datetime.time
    complaints: Optional[str]
    diagnosis: Optional[str]
    treatment: Optional[str]
    notes: Optional[str]
    cost: Optional[float]
    payment_status: Optional[str]
    branch_id: int

    class Config:
        orm_mode = True


class ServiceSchema(BaseModel):
    service_id: Optional[int]
    name: str
    description: Optional[str]
    price: float

    class Config:
        orm_mode = True


class AppointmentServicesSchema(BaseModel):
    appointment_id: int
    service_id: int
    amount: Optional[int]

    class Config:
        orm_mode = True


class DiseaseSchema(BaseModel):
    disease_id: Optional[int]
    name: str
    description: Optional[str]
    treatment: Optional[str]

    class Config:
        orm_mode = True


class AppointmentDiseasesSchema(BaseModel):
    appointment_id: int
    disease_id: int

    class Config:
        orm_mode = True


class MedicationSchema(BaseModel):
    medication_id: Optional[int]
    name: str
    description: Optional[str]
    dosage_info: Optional[str]

    class Config:
        orm_mode = True


class PrescriptionSchema(BaseModel):
    prescription_id: Optional[int]
    appointment_id: int
    date_issued: str
    notes: Optional[str]

    class Config:
        orm_mode = True


class PrescriptionMedicationsSchema(BaseModel):
    prescription_id: int
    medication_id: int
    dosage: Optional[str]
    instructions: Optional[str]
    is_available: Optional[bool]

    class Config:
        orm_mode = True
