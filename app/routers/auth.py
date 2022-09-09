from os import access
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models 
from .. import database
from .. import schemas, models, utils, oauth2
router = APIRouter(tags=['Authentication'])

@router.get('/login', response_model=schemas.Token)
def login (user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): 
  # OAuth2PasswordRequestForm but now we do not use schemas.UserLogin anymore 
  # and FastAPI form has a different format {'username':..., 'password':...}
  # also you now should write the credentials in form-data section 
  user= db.query(models.User).filter(models.User.email == user_credentials.username).first()
  print(user)
  if not user: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    detail='invalid credentials')
  if not utils.verify(user_credentials.password, user.password): 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    detail='invalid credentials')
  
  access_token=oauth2.create_access_token(data={'user_id': user.id})

  return {"access_token":access_token, "token_type":"bearer"}



