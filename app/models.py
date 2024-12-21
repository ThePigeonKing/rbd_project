from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, Date, Time, DECIMAL
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Models (SQLAlchemy)

class Position(Base):
    __tablename__ = "position"
    position_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    medical_services = Column(Boolean, default=False)


class Clinic(Base):
    __tablename__ = "clinic"
    clinic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)


class Employee(Base):
    __tablename__ = "employee"
    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    position_id = Column(Integer, ForeignKey("position.position_id"), nullable=True)
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=True)


class OwnerAnimal(Base):
    __tablename__ = "owner_animal"
    owner_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    source_branch = Column(Integer, nullable=True)


class Animal(Base):
    __tablename__ = "animal"
    animal_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    species = Column(String(30), nullable=False)
    breed = Column(String(30), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    owner_id = Column(Integer, ForeignKey("owner_animal.owner_id"), nullable=True)
    diabetes = Column(Boolean, default=False)
    chronic_diseases = Column(Text, nullable=True)
    vaccinations = Column(Text, nullable=True)
    source_branch = Column(Integer, nullable=True)


class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animal.animal_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.employee_id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    complaints = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    cost = Column(DECIMAL(8, 2), nullable=True)
    payment_status = Column(String(20), nullable=True)
    branch_id = Column(Integer, nullable=False)


class Service(Base):
    __tablename__ = "service"
    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)


class AppointmentServices(Base):
    __tablename__ = "appointment_services"
    appointment_id = Column(Integer, ForeignKey("appointment.appointment_id"), primary_key=True)
    service_id = Column(Integer, ForeignKey("service.service_id"), primary_key=True)
    amount = Column(Integer, nullable=True)


class Disease(Base):
    __tablename__ = "disease"
    disease_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)


class AppointmentDiseases(Base):
    __tablename__ = "appointment_diseases"
    appointment_id = Column(Integer, ForeignKey("appointment.appointment_id"), primary_key=True)
    disease_id = Column(Integer, ForeignKey("disease.disease_id"), primary_key=True)


class Medication(Base):
    __tablename__ = "medication"
    medication_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    dosage_info = Column(String(100), nullable=True)


class Prescription(Base):
    __tablename__ = "prescription"
    prescription_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointment.appointment_id"), nullable=False)
    date_issued = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)


class PrescriptionMedications(Base):
    __tablename__ = "prescription_medications"
    prescription_id = Column(Integer, ForeignKey("prescription.prescription_id"), primary_key=True)
    medication_id = Column(Integer, ForeignKey("medication.medication_id"), primary_key=True)
    dosage = Column(String(20), nullable=True)
    instructions = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)

