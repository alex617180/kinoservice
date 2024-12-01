# config/components/database.py
# Определение настроек базы данных для приложения.

import os
from config.components.pydantic_config import primary_db_config, secondary_db_config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': primary_db_config.db_name,
        'USER': primary_db_config.db_user,
        'PASSWORD': primary_db_config.db_password.get_secret_value(),
        'HOST': primary_db_config.db_host,
        'PORT': primary_db_config.db_port,
        'OPTIONS': {
            'options': f"-c search_path={primary_db_config.search_path}"
        }
    },
    'secondary': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secondary_db_config.db_name,
        'USER': secondary_db_config.db_user,
        'PASSWORD': secondary_db_config.db_password.get_secret_value(),
        'HOST': secondary_db_config.db_host,
        'PORT': secondary_db_config.db_port,
    }
}