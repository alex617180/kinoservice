FROM python:3.12

EXPOSE 8000

WORKDIR /web/django_admin

# Install system dependencies
RUN apt-get update && apt-get install -y sqlite3

# Copying the project files
COPY ./django_admin .

COPY .env ./config/.env
COPY ./docker_data/django_admin/run_uwsgi.sh .
COPY ./docker_data/django_admin/uwsgi.ini .
RUN chmod +x run_uwsgi.sh

# Create log, media and static directories and install dependencies
RUN mkdir -p /var/log/uwsgi && chmod -R 755 /var/log/uwsgi \
    && mkdir -p ./static ./media \
    && chown -R www-data:www-data ./static ./media \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/web/django_admin/run_uwsgi.sh"]

