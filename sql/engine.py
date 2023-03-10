from sqlalchemy import create_engine
from sqlalchemy import URL

from conf import username_db, password_db, host_db, database

url_object = URL.create(
    "postgresql+psycopg2",
    username=username_db,
    password=password_db,
    host=host_db,
    database=database,
)

engine = create_engine(url_object)
# engine = create_engine(url_object, echo=True)