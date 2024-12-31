from db.db_url import DATABASE_URL
from db.db_models import Base
from db.db_populate import populate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def init_db():
    print("DB initiation started")
    engine = create_engine(DATABASE_URL)
    # TODO: DB existance check
    if True: #not database_exists(engine.url):
        print("DB doesn't exist. Creation process started.")
        #create_database(engine.url)
        Base.metadata.create_all(engine)
        populate()
    print("DB initiation finished")


def get_session():
    engine = create_engine(DATABASE_URL)
    session = sessionmaker(bind=engine)
    return session()