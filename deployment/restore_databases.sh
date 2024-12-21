#!/bin/bash

# Директория с дампами на хосте
BACKUP_DIR="./backups"

# Проверка наличия бэкапов
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backup directory $BACKUP_DIR does not exist!"
    exit 1
fi

# Восстановление главного офиса
echo "Restoring main_office_db..."
docker cp ${BACKUP_DIR}/main_office_backup.dump main_office_db:/tmp/main_office_backup.dump
docker exec -t main_office_db pg_restore -U main_office_user -d main_office_db --clean --verbose /tmp/main_office_backup.dump
docker exec -t main_office_db rm /tmp/main_office_backup.dump

# Восстановление филиалов
for branch in 1 2 3; do
    BACKUP_FILE="${BACKUP_DIR}/branch_${branch}_backup.dump"
    if [ -f "$BACKUP_FILE" ]; then
        echo "Restoring branch_${branch}_db..."
        docker cp ${BACKUP_FILE} branch_${branch}_db:/tmp/branch_${branch}_backup.dump
        docker exec -t branch_${branch}_db pg_restore -U branch_${branch}_user -d branch_${branch}_db --clean --verbose /tmp/branch_${branch}_backup.dump
        docker exec -t branch_${branch}_db rm /tmp/branch_${branch}_backup.dump
    else
        echo "Warning: Backup file for branch_${branch} not found. Skipping."
    fi
done

echo "Restore complete!"

