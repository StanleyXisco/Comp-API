# from fastapi.testclient import TestClient
# import pytest

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# from app.database import get_db
# from app.database import Base
# from app.main import app


# from app.config import settings
# from alembic import command



# # creating a new database url for testing purposes, which is different from the development database, to avoid any conflicts between the two databases when running tests.

# # this is the database url for the testing database, which is different from the development database, to avoid any conflicts between the two databases when running tests.
# sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test" 
# # sqlalchemy_database_url = 'postgresql://postgres:password123@localhost:5432/myfastapi_test' # this is the database url for the testing database, which is different from the development database, to avoid any conflicts between the two databases when running tests.

# engine = create_engine(url=sqlalchemy_database_url)

# Testing_LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)



# # Base.metadata.create_all(bind=engine)




# # def override_get_db():
# #     db = Testing_LocalSession()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # app.dependency_overrides[get_db] = override_get_db


# #this fixture will return the database object, in case i want to manipulate data directly
# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = Testing_LocalSession()
#     try:
#         yield db
#     finally:
#         db.close()



# # this fixture will be used to create a new database for testing purposes, and drop the database after the tests are done, to avoid any conflicts with the development database.
# # the fixture is setup in such a way that it will run before the tests are run, and drop the database after the tests are done, to ensure that the testing database is clean and ready for the next test run.
# @pytest.fixture() # this will ensure that the fixture is run for each test function, and the database is dropped after each test function is done, to ensure that the testing database is clean and ready for the next test run.
# def client(session):
#     # #run our code before we run our test
#     # Base.metadata.create_all(bind=engine) # this method will be used to override the get_db dependency in the app, so that we can use a different database for testing purposes, and avoid any conflicts with the development database.
#     # yield TestClient(app)
#     # # run our code after our test finishes
#     # Base.metadata.drop_all(bind=engine)
#     def override_get_db():
    
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
    
#     yield TestClient(app) #this will return a brand new test client for each test function, which will use the same session object for the database connection, and the session object will be closed after each test function is done, to ensure that the testing database is clean and ready for the next test run.

