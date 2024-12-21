-- Заполнение таблицы "Должность"
INSERT INTO position (title, description, medical_services)
VALUES
    ('Veterinarian', 'Provides medical care to animals.', TRUE),
    ('Receptionist', 'Manages appointments and handles front desk tasks.', FALSE),
    ('Cleaner', 'Ensures the clinic is clean and hygienic.', FALSE);

-- Заполнение таблицы "Клиника"
INSERT INTO clinic (name, address, phone, email)
VALUES
    ('Central Clinic', '123 Main St, City Center', '123-456-7890', 'central@clinic.com'),
    ('Eastside Clinic', '456 East St, Suburb', '987-654-3210', 'eastside@clinic.com'),
    ('Westside Clinic', '789 West St, Downtown', '555-555-5555', 'westside@clinic.com');

-- Заполнение таблицы "Сотрудник"
INSERT INTO employee (first_name, last_name, phone, email, position_id, clinic_id)
VALUES
    ('John', 'Doe', '123-456-7891', 'john.doe@clinic.com', 1, 1),
    ('Jane', 'Smith', '987-654-3211', 'jane.smith@clinic.com', 2, 2),
    ('Emily', 'Davis', '555-555-5556', 'emily.davis@clinic.com', 3, 3);

-- Заполнение таблицы "Услуги"
INSERT INTO service (name, description, price)
VALUES
    ('General Checkup', 'Routine health checkup for animals.', 50.00),
    ('Vaccination', 'Administration of vaccines.', 30.00),
    ('Surgery', 'Minor or major surgical procedures.', 200.00);

-- Заполнение таблицы "Заболевания"
INSERT INTO disease (name, description, treatment)
VALUES
    ('Canine Distemper', 'A viral disease affecting dogs.', 'Antiviral treatment and supportive care.'),
    ('Feline Leukemia', 'A viral disease affecting cats.', 'Antiviral medication and immune support.'),
    ('Rabies', 'A deadly viral disease.', 'Immediate vaccination and quarantine.');

-- Заполнение таблицы "Препараты"
INSERT INTO medication (name, description, dosage_info)
VALUES
    ('Amoxicillin', 'Antibiotic for treating bacterial infections.', '250mg twice daily'),
    ('Metacam', 'Pain relief and anti-inflammatory medication.', '0.1mg/kg once daily'),
    ('Ivermectin', 'Medication for parasitic infestations.', '0.2mg/kg once monthly');
