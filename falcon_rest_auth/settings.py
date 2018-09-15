try:
    from .local_settings import *
except ImportError:
    from local_settings import *

from sqlalchemy import create_engine

DB_ENGINE = create_engine('{engine}://{username}:{password}@{host}:{port}/{db_name}'.format(**MARIADB) )

PROJECT_NAME = 'falcon_rest_auth'
