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
-- Максимальное количество слотов репликации
ALTER SYSTEM SET max_replication_slots = 5;
-- Максимальное количество рабочих процессов репликации
ALTER SYSTEM SET max_wal_senders = 5;
-- Таймаут для подтверждения репликации
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
    IF NEW.source_branch IS NOT NULL THEN
        -- Распространяем изменения на филиалы, кроме источника
        IF NEW.source_branch != 1 THEN
            PERFORM dblink_exec('dbname=branch_1_db', 'INSERT INTO owner_animal (...) VALUES (...)');
        END IF;
        IF NEW.source_branch != 2 THEN
            PERFORM dblink_exec('dbname=branch_2_db', 'INSERT INTO owner_animal (...) VALUES (...)');
        END IF;
        IF NEW.source_branch != 3 THEN
            PERFORM dblink_exec('dbname=branch_3_db', 'INSERT INTO owner_animal (...) VALUES (...)');
        END IF;
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
    -- Проверяем, что запись привязана к существующему owner_id
    IF NEW.owner_id IS NOT NULL THEN
        -- Распространяем изменения на филиалы, кроме источника
        IF NEW.source_branch != 1 THEN
            PERFORM dblink_exec('dbname=branch_1_db', 'INSERT INTO animal (...) VALUES (...)');
        END IF;
        IF NEW.source_branch != 2 THEN
            PERFORM dblink_exec('dbname=branch_2_db', 'INSERT INTO animal (...) VALUES (...)');
        END IF;
        IF NEW.source_branch != 3 THEN
            PERFORM dblink_exec('dbname=branch_3_db', 'INSERT INTO animal (...) VALUES (...)');
        END IF;
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
