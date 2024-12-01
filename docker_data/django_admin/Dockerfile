FROM python:3.12

WORKDIR /web/django_admin

# Копирование проекта
COPY ./django_admin /web/django_admin

# Создание папок для логов, статики и медиа
# Копирование зависимостей и установка пакетов
RUN  mkdir -p /var/log/uwsgi && chmod -R 755 /var/log/uwsgi \
     && mkdir -p /web/django_admin/static /web/django_admin/media \
     && chown -R www-data:www-data /web/django_admin/static /web/django_admin/media \
     && pip install --upgrade pip \
     && pip install --no-cache-dir -r /web/django_admin/requirements.txt


# Копирование файла с переменными окружения
COPY .env /web/django_admin/config/.env

# Копирование скрипта запуска
COPY ./docker_data/django_admin/run_uwsgi.sh /web/django_admin/run_uwsgi.sh
RUN chmod +x /web/django_admin/run_uwsgi.sh
# Копирование конфигурационного файла uWSGI
COPY ./docker_data/django_admin/uwsgi.ini /web/django_admin/uwsgi.ini

# Установка ENTRYPOINT для выполнения скрипта
ENTRYPOINT ["/web/django_admin/run_uwsgi.sh"]

EXPOSE 8000
