from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


# SQLALCHEMY_DATABASE_URL = f"postgresql://{
#     env('DATABASE_USERNAME')}:{env('DATABASE_PASSWORD')}@{env('DATABASE_HOST')}/{env('DATABASE_NAME')}"


SQLALCHEMY_DATABASE_URL = env('DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
