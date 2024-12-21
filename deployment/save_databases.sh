#!/bin/bash

# Создаем директорию для бэкапов на хосте
mkdir -p backups

# Главный офис
docker exec -t main_office_db mkdir -p /backups
docker exec -t main_office_db pg_dump -U main_office_user -F c -b -v -f /backups/main_office_backup.dump main_office_db
docker cp main_office_db:/backups/main_office_backup.dump ./backups/

# Филиалы
for branch in 1 2 3; do
    docker exec -t branch_${branch}_db mkdir -p /backups
    docker exec -t branch_${branch}_db pg_dump -U branch_${branch}_user -F c -b -v -f /backups/branch_${branch}_backup.dump branch_${branch}_db
    docker cp branch_${branch}_db:/backups/branch_${branch}_backup.dump ./backups/
done

echo "Backup complete!"

