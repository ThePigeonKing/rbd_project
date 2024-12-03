-- Создание таблицы "Должность"
CREATE TABLE position (
    position_id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    medical_services BOOLEAN
);

-- Создание таблицы "Клиника"
CREATE TABLE clinic (
    clinic_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL
);

-- Создание таблицы "Сотрудник"
CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    position_id INT,  -- В филиале не будет внешнего ключа на таблицу "position"
    clinic_id INT,    -- В филиале не будет внешнего ключа на таблицу "clinic"
    -- Убираем внешние ключи, т.к. данные о должностях и клиниках будут синхронизированы из головного офиса
    FOREIGN KEY (position_id) REFERENCES position (position_id) ON DELETE SET NULL,
    FOREIGN KEY (clinic_id) REFERENCES clinic (clinic_id) ON DELETE SET NULL
);

-- Создание таблицы "ВладелецЖивотное"
CREATE TABLE owner_animal (
    owner_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL
);

-- Создание таблицы "Животное"
CREATE TABLE animal (
    animal_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    species VARCHAR(30) NOT NULL,
    breed VARCHAR(30) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    owner_id INT,
    diabetes BOOLEAN,
    chronic_diseases TEXT,
    vaccinations TEXT
);

-- Создание таблицы "Прием"
CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    animal_id INT NOT NULL,
    employee_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    complaints TEXT,
    diagnosis TEXT,
    treatment TEXT,
    notes TEXT,
    cost DECIMAL(8, 2),
    payment_status VARCHAR(20),
    FOREIGN KEY (animal_id) REFERENCES animal (animal_id),
    FOREIGN KEY (employee_id) REFERENCES employee (employee_id)
);

-- Создание таблицы "Услуга"
CREATE TABLE service (
    service_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    price DECIMAL(8, 2) NOT NULL
);

-- Создание таблицы "УслугиПриема"
CREATE TABLE appointment_services (
    appointment_id INT NOT NULL,
    service_id INT NOT NULL,
    amount INT,
    PRIMARY KEY (appointment_id, service_id),
    FOREIGN KEY (appointment_id) REFERENCES appointment (appointment_id),
    FOREIGN KEY (service_id) REFERENCES service (service_id)
);

-- Создание таблицы "Заболевания"
CREATE TABLE disease (
    disease_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    treatment TEXT
);

-- Создание таблицы "ЗаболеванияПриема"
CREATE TABLE appointment_diseases (
    appointment_id INT NOT NULL,
    disease_id INT NOT NULL,
    PRIMARY KEY (appointment_id, disease_id),
    FOREIGN KEY (appointment_id) REFERENCES appointment (appointment_id),
    FOREIGN KEY (disease_id) REFERENCES disease (disease_id)
);

-- Создание таблицы "Препарат"
CREATE TABLE medication (
    medication_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    dosage_info VARCHAR(100)
);

-- Создание таблицы "Рецепт"
CREATE TABLE prescription (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL,
    date_issued DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (appointment_id) REFERENCES appointment (appointment_id)
);

-- Создание таблицы "РецептПрепараты"
CREATE TABLE prescription_medications (
    prescription_id INT NOT NULL,
    medication_id INT NOT NULL,
    dosage VARCHAR(20),
    instructions TEXT,
    is_available BOOLEAN,
    PRIMARY KEY (prescription_id, medication_id),
    FOREIGN KEY (prescription_id) REFERENCES prescription (prescription_id),
    FOREIGN KEY (medication_id) REFERENCES medication (medication_id)
);

