from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME

DATABASE_URL = rf'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)
session = DBSession()
