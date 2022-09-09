from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# since we have alembic that already creates the tables we no longer need sqlalchemy engine
# models.Base.metadata.create_all(bind=engine)

# what domains can speak to our APi 
origins = [
    "http://localhost:8080", 
    "https://www.google.com"
]
# if you want public API 
origins=['*']

app=FastAPI()
app.add_middleware(
  # basicly a fucntion that runs after request, so if someone sends the request to our app before in goes through routers it goes here 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# the request is going to go the post router object and find the url
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

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


# def find_posts(id):
#   for p in my_posts: 
#     if p['id']==id:
#       return p

# def find_index_post(id):
#   for i,p in enumerate(my_posts): 
#     if p['id']==id:
#       return i

# Path operation/root
# Decorator, which is routerlied to a function, which makes this fucntion a path operation 
# a- decorator, the name, get - HTTP method that a user should use, ('/') - roote path
# if i create smt @router.get('/login') it means that this path operation will only apply if a user goes to this url
@app.get("/")
# Fisrt - function
# async - asynchronosly, can delete it 
# root is just a name
async def root():
    # the data taht get sent to the user, fast API will automaticly convert it to JSON
    return {"message": "welcome to my api!!!"}






