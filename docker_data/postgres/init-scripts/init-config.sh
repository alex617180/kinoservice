#!/bin/bash
echo "Настраиваем доступ к PostgreSQL..."

# Добавляем разрешения для всех хостов в pg_hba.conf
echo "host    all             all             0.0.0.0/0            md5" >> "$PGDATA/pg_hba.conf"

# Изменяем настройку listen_addresses в postgresql.conf
echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"
