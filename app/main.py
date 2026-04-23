from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# print(settings)


# creating the tables in the database using the models defined in models.py
#models.Base.metadata.create_all(bind=engine) # since i already setup alembic to handle data migrations, i can comment this out to avoid any conflicts between the two methods of handling database schema changes.

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# my_post = [{"title": "favorite sport", "content": "I love to play football", "id": 1},
#            {"title": "favorite food", "content": "I like fufu and uchakuru soup", "id": 2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my api!!"}



