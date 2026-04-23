from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
# from .settings import settings

Base = declarative_base()

sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(url=sqlalchemy_database_url)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Dependency to get a database session using SQLAlchemy
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

# # Connection to database usong psycopg2
# while True:
    
#     try:
#         conn = psycopg2.connect(host='localhost', database='myfastapi', user='postgres',
#                                  password='', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(3)