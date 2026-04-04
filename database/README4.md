# 📦 Экспорт и импорт базы данных

## Команды

### Экспорт из БД → файл
```bash
docker exec -i car_parts_db pg_dump -U myuser --clean --if-exists parts_catalog > full_backup.sql
```

### Импорт из файла → БД
```bash
iconv -f UTF-16LE -t UTF-8 full_backup.sql > full_backup_utf8.sql
mv full_backup_utf8.sql full_backup.sql
docker exec -i car_parts_db psql -U myuser -d parts_catalog < full_backup.sql
```

---

## Порядок действий при передаче данных между ПК

### На исходном ПК (отправка):
```bash
# 1. Сделать дамп
docker exec -i car_parts_db pg_dump -U myuser --clean --if-exists parts_catalog > full_backup.sql

# 2. Передать файл full_backup.sql на другой ПК
```

### На целевом ПК (получение):
```bash
# 1. Запустить контейнер
docker-compose up -d

# 2. Конвертировать UTF-16 → UTF-8 (обязательно!)
iconv -f UTF-16LE -t UTF-8 full_backup.sql > full_backup_utf8.sql
mv full_backup_utf8.sql full_backup.sql

# 3. Загрузить в БД
docker exec -i car_parts_db psql -U myuser -d parts_catalog < full_backup.sql

# 4. Проверить
docker exec -it car_parts_db psql -U myuser -d parts_catalog -c "SELECT count(*) FROM parts_inventory;"
```

---

## Почему нужна конвертация

`docker exec` через WSL/PowerShell сохраняет файл в UTF-16. PostgreSQL требует UTF-8. Без `iconv` будет ошибка:
```
ERROR: invalid byte sequence for encoding "UTF8": 0xff
```
