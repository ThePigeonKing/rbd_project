# rbd_project
Project for HSE's subject "Distributed databases"


## Setup

### Репликация без основной копии (по подписке)

- Филиалы [1-3] → ГО: Каждое изменение, внесенное в филиале, реплицируется в головной офис.
- ГО → Филиалы [1-3]: ГО пересылает изменения, которые не пришли из филиала, только в оставшиеся филиалы

**На всех узлах базы данных:**
```sql
-- Уровень WAL для логической репликации
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET wal_sender_timeout = '60s';


SELECT pg_reload_conf();
```

| проверить при помощи `SHOW <VARIABLE>`

**На головном офисе:**

Создание публикации:
```sql
CREATE PUBLICATION main_office_pub
FOR TABLE owner_animal, animal;
```

Настройка подписок:
```sql
-- Подписка на филиал 1
CREATE SUBSCRIPTION branch_1_to_main_office
CONNECTION 'host=branch_1_db port=5432 user=branch_1_user password=branch_1_password dbname=branch_1_db'
PUBLICATION branch_1_pub;

-- Подписка на филиал 2
CREATE SUBSCRIPTION branch_2_to_main_office
CONNECTION 'host=branch_2_db port=5432 user=branch_2_user password=branch_2_password dbname=branch_2_db'
PUBLICATION branch_2_pub;

-- Подписка на филиал 3
CREATE SUBSCRIPTION branch_3_to_main_office
CONNECTION 'host=branch_3_db port=5432 user=branch_3_user password=branch_3_password dbname=branch_3_db'
PUBLICATION branch_3_pub;
```

Триггеры для отправки изменений только на нужные филиалы:
```sql
CREATE OR REPLACE FUNCTION replicate_owner_animal_to_branches()
RETURNS TRIGGER AS $$
BEGIN
    -- Определяем источник данных
    IF NEW.source_branch IS NULL THEN
        -- Если source_branch не указан (локальная вставка), отправляем изменения на все филиалы
        PERFORM dblink_exec('dbname=branch_1_db', 
            'INSERT INTO owner_animal (first_name, last_name, address, phone, email, source_branch)
             VALUES (' || quote_literal(NEW.first_name) || ', '
                          || quote_literal(NEW.last_name) || ', '
                          || quote_literal(NEW.address) || ', '
                          || quote_literal(NEW.phone) || ', '
                          || quote_literal(NEW.email) || ', 0)');

        PERFORM dblink_exec('dbname=branch_2_db', 
            'INSERT INTO owner_animal (first_name, last_name, address, phone, email, source_branch)
             VALUES (' || quote_literal(NEW.first_name) || ', '
                          || quote_literal(NEW.last_name) || ', '
                          || quote_literal(NEW.address) || ', '
                          || quote_literal(NEW.phone) || ', '
                          || quote_literal(NEW.email) || ', 0)');

        PERFORM dblink_exec('dbname=branch_3_db', 
            'INSERT INTO owner_animal (first_name, last_name, address, phone, email, source_branch)
             VALUES (' || quote_literal(NEW.first_name) || ', '
                          || quote_literal(NEW.last_name) || ', '
                          || quote_literal(NEW.address) || ', '
                          || quote_literal(NEW.phone) || ', '
                          || quote_literal(NEW.email) || ', 0)');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER replicate_owner_animal_to_branches_trigger
AFTER INSERT OR UPDATE ON owner_animal
FOR EACH ROW EXECUTE FUNCTION replicate_owner_animal_to_branches();
```
```sql
CREATE OR REPLACE FUNCTION replicate_animal_to_branches()
RETURNS TRIGGER AS $$
BEGIN
    -- Определяем источник данных
    IF NEW.source_branch IS NULL THEN
        -- Если source_branch не указан (локальная вставка), отправляем изменения на все филиалы
        PERFORM dblink_exec('dbname=branch_1_db', 
            'INSERT INTO animal (name, species, breed, date_of_birth, gender, owner_id, diabetes, chronic_diseases, vaccinations, source_branch)
             VALUES (' || quote_literal(NEW.name) || ', '
                          || quote_literal(NEW.species) || ', '
                          || quote_literal(NEW.breed) || ', '
                          || quote_literal(NEW.date_of_birth) || ', '
                          || quote_literal(NEW.gender) || ', '
                          || NEW.owner_id || ', '
                          || quote_literal(NEW.diabetes) || ', '
                          || quote_literal(NEW.chronic_diseases) || ', '
                          || quote_literal(NEW.vaccinations) || ', 0)');

        PERFORM dblink_exec('dbname=branch_2_db', 
            'INSERT INTO animal (name, species, breed, date_of_birth, gender, owner_id, diabetes, chronic_diseases, vaccinations, source_branch)
             VALUES (' || quote_literal(NEW.name) || ', '
                          || quote_literal(NEW.species) || ', '
                          || quote_literal(NEW.breed) || ', '
                          || quote_literal(NEW.date_of_birth) || ', '
                          || quote_literal(NEW.gender) || ', '
                          || NEW.owner_id || ', '
                          || quote_literal(NEW.diabetes) || ', '
                          || quote_literal(NEW.chronic_diseases) || ', '
                          || quote_literal(NEW.vaccinations) || ', 0)');

        PERFORM dblink_exec('dbname=branch_3_db', 
            'INSERT INTO animal (name, species, breed, date_of_birth, gender, owner_id, diabetes, chronic_diseases, vaccinations, source_branch)
             VALUES (' || quote_literal(NEW.name) || ', '
                          || quote_literal(NEW.species) || ', '
                          || quote_literal(NEW.breed) || ', '
                          || quote_literal(NEW.date_of_birth) || ', '
                          || quote_literal(NEW.gender) || ', '
                          || NEW.owner_id || ', '
                          || quote_literal(NEW.diabetes) || ', '
                          || quote_literal(NEW.chronic_diseases) || ', '
                          || quote_literal(NEW.vaccinations) || ', 0)');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER replicate_animal_to_branches_trigger
AFTER INSERT OR UPDATE ON animal
FOR EACH ROW EXECUTE FUNCTION replicate_animal_to_branches();
```


**На филиалах:**

Создание публикаций:
```sql
CREATE PUBLICATION branch_1_pub FOR TABLE owner_animal, animal;
CREATE PUBLICATION branch_2_pub FOR TABLE owner_animal, animal;
CREATE PUBLICATION branch_3_pub FOR TABLE owner_animal, animal;
```

Создание подписок:
```sql
-- На филиале 1
CREATE SUBSCRIPTION main_office_to_branch_1
CONNECTION 'host=main_office_db port=5432 user=main_office_user password=main_office_password dbname=main_office_db'
PUBLICATION main_office_pub;

-- На филиале 2
CREATE SUBSCRIPTION main_office_to_branch_2
CONNECTION 'host=main_office_db port=5432 user=main_office_user password=main_office_password dbname=main_office_db'
PUBLICATION main_office_pub;

-- На филиале 3
CREATE SUBSCRIPTION main_office_to_branch_3
CONNECTION 'host=main_office_db port=5432 user=main_office_user password=main_office_password dbname=main_office_db'
PUBLICATION main_office_pub;
```

### Репликация с консолидацией + удаленный запрос

Просто добавить к уже существующей публикации таблицу appointment:
```
ALTER PUBLICATION branch_X_pub ADD TABLE appointment;

ALTER PUBLICATION main_office_pub ADD TABLE appointment;
```

И теперь можно использовать удаленный запрос:
```
SELECT * FROM dblink('main_office_conn',
                     'SELECT * FROM appointment WHERE animal_id = 123')
AS t(appointment_id INTEGER, animal_id INTEGER, employee_id INTEGER, branch_id INTEGER, appointment_date DATE, appointment_time TIME, complaints TEXT, diagnosis TEXT, treatment TEXT, notes TEXT, cost DECIMAL, payment_status VARCHAR);
```

### РОК один раз в день

#### Вспомогательные команды

Список подписок и публикаций в БД:
```sql
SELECT * FROM pg_stat_subscription;
SELECT * FROM pg_publication;
```

Добавить source_branch к нужным таблицам:
```sql
ALTER TABLE owner_animal ADD COLUMN source_branch INTEGER DEFAULT NULL;
ALTER TABLE animal ADD COLUMN source_branch INTEGER DEFAULT NULL;
ALTER TABLE appointment ADD COLUMN branch_id INTEGER NOT NULL;
```

Перезагрузить подписки после восстановления данных:
```sql
--- ГО
ALTER SUBSCRIPTION branch_1_to_main_office ENABLE;
ALTER SUBSCRIPTION branch_2_to_main_office ENABLE;
ALTER SUBSCRIPTION branch_3_to_main_office ENABLE;

--- ГО
ALTER SUBSCRIPTION branch_1_to_main_office REFRESH PUBLICATION;
ALTER SUBSCRIPTION branch_2_to_main_office REFRESH PUBLICATION;
ALTER SUBSCRIPTION branch_3_to_main_office REFRESH PUBLICATION;

--- филиалы
ALTER SUBSCRIPTION main_office_to_branch_1 REFRESH PUBLICATION;
ALTER SUBSCRIPTION main_office_to_branch_2 REFRESH PUBLICATION;
ALTER SUBSCRIPTION main_office_to_branch_3 REFRESH PUBLICATION;
```

#### Вспомогательные функции

Удалить все триггеры и функции:
```sql
-- удаление старого триггер для таблицы owner_animal
DROP TRIGGER IF EXISTS replicate_owner_animal_to_branches_trigger ON owner_animal;

-- удаление старого триггер для таблицы animal
DROP TRIGGER IF EXISTS replicate_animal_to_branches_trigger ON animal;

-- удаление старого функции триггеров
DROP FUNCTION IF EXISTS replicate_owner_animal_to_branches CASCADE;
DROP FUNCTION IF EXISTS replicate_animal_to_branches CASCADE;
```

#### Бекап и восстановление

Два sh были созданы для автоматического сохранения и восстановления состояния баз данных:
```bash
.
├── backups         # папка с sql дампами состояний баз данных
│   ├── branch_1_backup.dump
│   ├── branch_2_backup.dump
│   ├── branch_3_backup.dump
│   └── main_office_backup.dump
├── branch_db_init.sql          # скрипт для создания таблиц в филиале
├── data            # папка с примонтированными разеделами docker
│   ├── branch_1  [error opening dir]
│   ├── branch_2  [error opening dir]
│   ├── branch_3  [error opening dir]
│   └── main_office  [error opening dir]
├── docker-compose.yaml
├── drop_all_tables.sql         # скрипт обнуления всех баз данных
├── main_office_db_init.sql     # скрипт для создания таблиц в головоном офисе
├── restore_databases.sh        # скрипт восстановления баз данных из дампов
└── save_databases.sh           # скрипт сохранения дампов баз данных
```


