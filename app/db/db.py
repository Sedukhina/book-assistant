from db.db_url import DATABASE_URL
from db.db_models import Base
from db.db_populate import populate

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def init_db():
    engine = create_engine(DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
        #populate()
    