from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.database import get_db
from app.database import Base
from app.main import app
from app.routers.Oauth2 import create_access_token
from app import models


from app.config import settings
from alembic import command



# creating a new database url for testing purposes, which is different from the development database, to avoid any conflicts between the two databases when running tests.

# this is the database url for the testing database, which is different from the development database, to avoid any conflicts between the two databases when running tests.
sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test" 
# sqlalchemy_database_url = 'postgresql://postgres:password123@localhost:5432/myfastapi_test' # this is the database url for the testing database, which is different from the development database, to avoid any conflicts between the two databases when running tests.

engine = create_engine(url=sqlalchemy_database_url)

Testing_LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)



# Base.metadata.create_all(bind=engine)




# def override_get_db():
#     db = Testing_LocalSession()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


#this fixture will return the database object, in case i want to manipulate data directly
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_LocalSession()
    try:
        yield db
    finally:
        db.close()



# this fixture will be used to create a new database for testing purposes, and drop the database after the tests are done, to avoid any conflicts with the development database.
# the fixture is setup in such a way that it will run before the tests are run, and drop the database after the tests are done, to ensure that the testing database is clean and ready for the next test run.
@pytest.fixture() # this will ensure that the fixture is run for each test function, and the database is dropped after each test function is done, to ensure that the testing database is clean and ready for the next test run.
def client(session):
    # #run our code before we run our test
    # Base.metadata.create_all(bind=engine) # this method will be used to override the get_db dependency in the app, so that we can use a different database for testing purposes, and avoid any conflicts with the development database.
    # yield TestClient(app)
    # # run our code after our test finishes
    # Base.metadata.drop_all(bind=engine)
    def override_get_db():
    
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app) #this will return a brand new test client for each test function, which will use the same session object for the database connection, and the session object will be closed after each test function is done, to ensure that the testing database is clean and ready for the next test run.

@pytest.fixture
def test_user2(client):
    userData = {"email": "test24@example.com", "password": "password123"}

    response = client.post("/users/", json=userData)

    assert response.status_code == 201
    
    new_user = response.json()
    new_user["password"] = userData["password"]
    return new_user

@pytest.fixture
def test_user(client):
    userData = {"email": "test@example.com", "password": "password123"}

    response = client.post("/users/", json=userData)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = userData["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "first post", "content": "first content", "owner_id": test_user['id']},
        {"title": "second post", "content": "second content", "owner_id": test_user['id']},
        {"title": "third post", "content": "third content", "owner_id": test_user['id']},
        {"title": "fourth post", "content": "fourth content", "owner_id": test_user2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()