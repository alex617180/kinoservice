#!/bin/bash

# Остановить выполнение скрипта при ошибке
set -e

# Логирование
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Проверка базы данных
# log "Проверяем доступность базы данных..."
# ATTEMPTS=0
# MAX_ATTEMPTS=10
# until python manage.py dbshell -c "SELECT 1" &>/dev/null; do
#   if [ $ATTEMPTS -ge $MAX_ATTEMPTS ]; then
#     log "База данных недоступна после $MAX_ATTEMPTS попыток. Завершаем работу."
#     exit 1
#   fi
#   ATTEMPTS=$((ATTEMPTS+1))
#   log "База данных недоступна, повторяем попытку ($ATTEMPTS/$MAX_ATTEMPTS)..."
#   sleep 5
# done
# log "База данных доступна."

# Создание основной базы данных, если она отсутствует
# log "Проверяем существование базы данных '${PRIMARY_DB_NAME}'..."
# DB_EXISTS=$(psql -h $PRIMARY_DB_HOST -U $PRIMARY_DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '${PRIMARY_DB_NAME}';")
# if [ -z "$DB_EXISTS" ]; then
#   log "База данных '${PRIMARY_DB_NAME}' отсутствует. Создаем..."
#   psql -h $PRIMARY_DB_HOST -U $PRIMARY_DB_USER -c "CREATE DATABASE ${PRIMARY_DB_NAME};"
# else
#   log "База данных '${PRIMARY_DB_NAME}' уже существует."
# fi

# Выполнение миграций
# log "Выполняем миграции..."
# python manage.py migrate --noinput

# log "Создаем суперпользователя, если он еще не существует..."
# python manage.py shell <<EOF
# from django.contrib.auth import get_user_model
# import os
# User = get_user_model()
# if not User.objects.filter(username=os.getenv('SUPERUSER_NAME')).exists():
#     User.objects.create_superuser(
#         username=os.getenv('SUPERUSER_NAME'),
#         email=os.getenv('SUPERUSER_EMAIL'),
#         password=os.getenv('SUPERUSER_PASSWORD')
#     )
#     print(f"Суперпользователь '{os.getenv('SUPERUSER_NAME')}' создан.")
# else:
#     print(f"Суперпользователь '{os.getenv('SUPERUSER_NAME')}' уже существует.")
# EOF

# Сбор статических файлов
log "Собираем статические файлы..."
python manage.py collectstatic --no-input

chown -R www-data:www-data /web/django_admin/static /web/django_admin/media

# Запуск uWSGI
log "Запускаем uWSGI..."
exec uwsgi --strict --ini uwsgi.ini
