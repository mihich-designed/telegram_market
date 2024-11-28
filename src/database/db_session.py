from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

db_path = os.getenv('DB_LOCAL_PATH')
engine = create_engine(f'sqlite:///{db_path}')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def get_session():
    return Session()