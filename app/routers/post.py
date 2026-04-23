from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
from . import Oauth2

from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/", response_model=List[schemas.PostResponse])
# @router.get("/")
def get_post(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user),
             limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # implementing raw sql query to get all posts using psycopg2
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    # Implementation of same query using sqlalchemy
    # this also implements pagination and search functionality using sqlalchemy, the limit parameter limits the number of posts returned,
    # the offset parameter skips the first n posts, and the search parameter filters the posts based on the title containing the search string.

    """
    Fetch all posts with vote count, supporting pagination and search.
    """
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,
        models.Vote.post_id ==  models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # results1 = [
    #     {
    #         "Post": post,
    #         "votes": votes or 0
    #     }
    #     for post, votes in results
    # ]
    # print(results)
    return posts

    # we can implement a scenario where we only want to return the posts that belong to the current user,
    # this is useful for authentication and authorization purposes, as it allows us to ensure that users can only access their own posts and not the posts of other users.
    # but that is not the logic i intend to implement for this endpoint.
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0, 1000000)
    # my_post.append(post_dict)

    # title str, content str, published bool
    # implementing raw sql query to create a post using psycopg2
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Implementation of same query using sqlalchemy
    # added the owner_id field to the post object to associate the post with the user who created it, 
    # this is important for authentication and authorization purposes, as it allows us to determine which user created which post and enforce access control accordingly.


    new_post = models.Post(owner_id=current_user.id, **post.model_dump())     # unpacking the post object to create a new post object that can be added to the database.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    # implementing raw sql query to get a post by id using psycopg2
    # convert id to string because the sql query is a string and it expects a string
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    # Implementation of same query using sqlalchemy
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,
        models.Vote.post_id ==  models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")  
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # deleting post
    # find the index in the array that has required id
    # my_post.pop(index)

    # implementing raw sql query to delete a post by id using psycopg2
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"post with id: {id} was not found")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Implementation of same query using sqlalchemy
    dl_post = db.query(models.Post).filter(models.Post.id == id)


    if dl_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    # check if the user who is trying to delete the post is the owner of the post,
    # if not, then we can return an error message saying that they are not authorized to perform this action.
    if dl_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")

    dl_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    # Implementing raw sql query to update a post by id using psycopg2

    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # implementation of same query using sqlalchemy

    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    # check if the user who is trying to update the post is the owner of the post,
    # if not, then we can return an error message saying that they are not authorized to perform this action.
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
    
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
       
    return updated_post.first()