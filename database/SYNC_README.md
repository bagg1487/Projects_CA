# 🔄 Git-sync для базы данных

Автоматическая синхронизация PostgreSQL между устройствами через GitHub.

## Быстрый старт

### Первое устройство (откуда синхронизировать)

```bash
# 1. Убедись что Docker запущен и БД работает
docker-compose up -d

# 2. Сделай дамп и запушь в Git
cd database/
chmod +x sync_push.sh sync_pull.sh
./sync_push.sh "initial: первый дамп БД"
```

### Второе устройство (куда синхронизировать)

```bash
# 1. Клонируй репозиторий
git clone <URL> Projects_CA
cd Projects_CA/database/

# 2. Запусти синхронизацию (pull + restore БД)
chmod +x sync_push.sh sync_pull.sh
./sync_pull.sh
```

Готово! Все записи с первого устройства теперь на втором.

---

## Скрипты

### `sync_push.sh` — Отправить изменения

```bash
./sync_push.sh ["Описание изменений"]
```

## Настройка GitHub

### 1. Создай приватный репозиторий на GitHub

```
GitHub → New repository → Private → Create
```

### 2. Добавь remote

```bash
cd /path/to/Projects_CA
git remote add origin git@github.com:username/Projects_CA.git
git branch -M main
git push -u origin main
```

### 3. На втором устройстве

```bash
git clone git@github.com:username/Projects_CA.git
cd Projects_CA/database/
./sync_pull.sh
```

---

## Рабочий процесс

### Сценарий: поработал на одном ПК → переходишь на другой

```
ПК-1 (работа закончена)          GitHub              ПК-2 (продолжаешь)
       │                           │                      │
  ./sync_push.sh  ─────────────►  commit  ◄──────────  ./sync_pull.sh
   (dump + commit + push)        (remote)              (pull + restore)
```

### Рекомендации

- **Перед выключением ПК** — запускай `./sync_push.sh`
- **Перед началом работы на новом ПК** — запускай `./sync_pull.sh`
- **Не работай одновременно на двух устройствах** — последний push перезаписывает БД

---

## Структура файлов

```
database/
├── sync_push.sh          # Экспорт → Git push
├── sync_pull.sh          # Git pull → Импорт
├── full_backup.sql       # Актуальный дамп (обновляется скриптами)
├── BD_dead_kolesa_kz.sql # Схема БД (для первого запуска)
├── docker-compose.yml    # PostgreSQL контейнер
└── migrations/           # SQL-миграции
```

---

## Troubleshooting

### Контейнер не запускается
```bash
docker-compose down -v    # Удалить volume
docker-compose up -d      # Пересоздать
./sync_pull.sh            # Восстановить БД
```

### Ошибка "remote origin not found"
```bash
git remote add origin git@github.com:username/repo.git
```

### Конфликт при git pull
```bash
git checkout -- database/full_backup.sql  # Взять локальную версию
git pull                                  # Повторить pull
./sync_pull.sh                            # Восстановить БД
```

### Дамп слишком большой для Git (>100MB)
Если БД разрастётся, используй [Git LFS](https://git-lfs.com/):
```bash
git lfs install
git lfs track "database/full_backup.sql"
git add .gitattributes
git commit -m "chore: добавить SQL дамп в LFS"
```

---

## Безопасность

⚠️ **Важно:** Пароль БД (`mypassword`) захардкожен в скриптах и `docker-compose.yml`.
Для приватного репозитория это допустимо, но для публичного — **обязательно** вынеси в `.env`:

```bash
# .env (НЕ коммитить в Git!)
POSTGRES_PASSWORD=your_secure_password
```

И обнови `docker-compose.yml`:
```yaml
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```
