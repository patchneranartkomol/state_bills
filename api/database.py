from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#TODO: determine how PostgreSQL DB is hosted in dev / prod
SQLALCHEMY_DATABASE_URL = "postgresql://patch@localhost/state_bills"

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
