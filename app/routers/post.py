from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

router=APIRouter(
  prefix='/posts',
  tags=['Posts']
)
# it will be stored in JSON in FastAPI()
my_posts=[{"title":"title of post 1", "content":"content of post 1", "id":1},
 {"title":"favorite foods", "content":"I like pizza", "id":2}]

while True:
  try: 
    conn=psycopg2.connect(host='localhost', database='fastapi', 
    user='postgres', password='utKirill2021199', cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print('DB connection was succesfull')
    break
  except Exception as error: 
    print('DB connection failed')
    print("Error:", error)
    time.sleep(2)



# @router.get("/sqlalchemy")
# # store in db variable call the Session and calls the get_db function
# def test_posts(db: Session = Depends(get_db)): 
#   posts=db.query(models.Post).all()
#   return {"Posts":posts}

# everytime we make a change we need to restart our server: for this in the termianl add --reload
# List because we request plenty of posts
@router.get("/", response_model=List[schemas.PostResponse])
# SQLALCHEMY JOINS FIRST OF ALL WE WOULD NEED A DIFFERENT SCHEMA FOR response models for results
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int = 10, skip: int = 0, search: Optional[str] = ""):
  # PSYCOPG2 EXAMPLE
  # cursor.execute("""SELECT * FROM posts""")
  # posts=cursor.fetchall()

  # SQLALCHEMY EXAMPLE
  # by default in sqlalchemy JOIN is LEFT INNER 
  results=db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  # if we wnat all posts with for some specific user
  # posts=db.query(models.Post.owner_id==current_user.id).all()\

  return results

# # So it is going to take all the fields in the body, cinverted it to dict and passed it into the variable payload
# # Usually a body is JSON format
# @router.post("/createposts")
# def create_posts(payload: dict=Body(...)):
#   print(payload)
#   return{'new_post':f"The structure: {payload.keys()}, the title: {payload['title']}, the content: {payload['content']}"}

# Fast API will automaticly checks the data the client post with Post pydantic class, 
# does it have a title? is it a string? 
# it is also automaticly printed out the structured data title='API' content='Look at this awesome API'
# new_post is a pydantic Model, and it has method .dict, will converted to a dictionary
# Also needs a defined status code

# CREATE A NEW POST 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # HARD CODE EXAMPLE

  # print(post)
  # print(post.dict())
  # post_dict=post.dict()
  # post_dict['id']=randrange(0, 100000000)
  # my_posts.routerend(post_dict)

  # PSYCOPG2 EXAMPLE 
  # NOW WITH DB, %s - to make sure no SQL injections will not effect the execution proccess 
  # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
  # new_post=cursor.fetchone()
  # # VERY IMPORTANT
  # conn.commit()

  # SQLALCHEMY EXAMPLE
  # new_post = models.Post(
  #         title=post.title, content=post.content, published=post.published) 
  print(current_user.email)
  new_post = models.Post(owner_id=current_user.id, **post.dict()) 
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


@router.get("/latest")
def get_latest_post(): 
  post=my_posts[-1]
  return{"latest_post":post}

# GET ONE POST HARDCODE AND PSYCOPG EXAMPLES
# # id fiels - is a path parameter
# a FastAPI has a good automatic validation if a it can not convert id to an integer wil
# throw an explanation of the error value is not a valid integer
# agaian the order matters because the {id} - is a path parameter it can be anything 
# so if we put the latest_post response after this one it will match 
# the get_post and throw an error because latest mathces the id path parameter
# if the id does not exists initially it will return null, but the stutus will be 200 OK
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id:int, user_id: int = Depends(oauth2.get_current_user)): #response: Response):
    # because the SQL query is a string so id also should be str
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    # post=find_posts(id) #very important initial id is a string
    if not post: 
      # or response.status_code = 404
      # response.status_code=status.HTTP_404_NOT_FOUND
      # return {'message':f'post with {id} was not found'}

      # More elegant way
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail= f'post with {id} was not found')
    return post

# GET ONE POST SQLALCHEMY EXAMPLE 
@router.get("/sqlalchemy/{id}", response_model=schemas.PostVote)
def get_post(id:int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  post=db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  if not post: 
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND , 
    detail=f'post with {id} id was not found')
  # if post.owner_id!=current_user.id: 
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')
  return post


# DELETE ONE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# *db variable for SQLALCHEMY 
def delete_post(id:int, user_id: int = Depends(oauth2.get_current_user)): 
  # HARDCODE EXAMPLE 
  # if we pass not existing id, the 500 error, because we put NoneType to pop
  # index=find_index_post(id)
  # my_posts.pop(index)

  # PSCOPG EXAMPLE
  cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))
  deleted_post=cursor.fetchone()
  conn.commit()

  # THE COMMON PART
  if deleted_post==None: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail=f'Post with {id} id was not found')
  # so 204 you don't send any data back so no message instead 
  return Response(status_code=status.HTTP_204_NO_CONTENT)

  # DELETE ONE POST SQLALCHEMY
@router.delete("/sqlalchemy/{id}")
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
  post_query=db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail=f"Post with {id} id was not found")
  if post.owner_id!=current_user.id: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    detail="Not authorized")
  post_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)


# PUT POST
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostBase, current_user: int = Depends(oauth2.get_current_user)):
  # HARDCODE EXAMPLE 
  # index=find_index_post(id)
  # post_dict=post.dict()
  # post_dict['id']=id
  # my_posts[index]=post_dict

  # PSYCOPG2 EXAMPLE 
  cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, str(id),))
  updated_post=cursor.fetchone()
  conn.commit()
  if updated_post==None: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail=f'Post with {id} id was not found')
  return updated_post

# PUT ONE POST SQLALCHEMY EXAMPLE 
@router.put("/sqlalchemy/{id}", response_model=schemas.PostResponse)
def update_post(id:int, pydantic_post:schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
  post_query=db.query(models.Post).filter(models.Post.id == id)
  post=post_query.first()
  print(post)
  if post == None: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail=f"Post with {id} id was not found")
  if post.owner_id != current_user.id: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    detail="Not authorized")
  # post_query.update({'title':'updated post', 'content':'the content of updated post'})
  post_query.update(pydantic_post.dict(), synchronize_session=False)
  db.commit()

  return post_query.first()