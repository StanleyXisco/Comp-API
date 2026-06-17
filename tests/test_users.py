import pytest
import jwt
from app import schemas
# from .database import client, session
from app.config import settings



def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to to this comprehensive application. Please add /docs to the current url to see the API documentation, but you will not be able to see the CI/CD pipeline documentation here."
    "Please check the README.md file for more information on how to access the CI/CD pipeline documentation."}


def test_create_user(client):
    response = client.post("/users/", json={"email": "test@example.com", "password": "password123"})

    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test@example.com"

def test_login_user(client,test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**response.json())
    #validation of the token, to ensure that the token is valid and can be decoded, and that the user id in the token matches the user id of the test user.
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    # Extract the user id from the payload
    id: int = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test@example.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test@example.com', None, 422)
    ])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json() == {"detail": "Invalid Credentials"} this would not apply when we get a 422 error, because the error message would be different, so we will not assert the error message in this test function, and only assert the status code.