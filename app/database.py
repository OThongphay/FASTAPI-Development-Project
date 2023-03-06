from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#Creates a database url for sqlalchemy
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#creates an engine using the url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#creates a session
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

#Creates a sessuib for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#While statement for reference to use this postgres library to run raw SQL with database driver
#while True:
#    try:
#        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'DarkSouls@87', cursor_factory = RealDictCursor)
#        cursor = conn.cursor()
#        print("Database connection successful")
#        break
#    except Exception as error: 
#        print("Connection to database Failed")
#        print("Error: ", error)
#        time.sleep(2)
