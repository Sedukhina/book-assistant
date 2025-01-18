from db.db_url import DATABASE_URL
from db.db_models import Base, BookBase
from db.db_populate import Populate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    engine = create_engine(DATABASE_URL)
    session = sessionmaker(bind=engine)
    return session()


def init_db():
    print("DB initiation started")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    if not session.query(BookBase).first():
        print("DB is empty. Population process started.")
        Populate()
        print("DB population  finished")

    print("DB initiation finished")
