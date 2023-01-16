import dj_database_url
from decouple import config

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'), conn_max_age=600),
}
DEBUG = True
