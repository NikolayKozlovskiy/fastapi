from pydantic import BaseSettings

# We set environment varibales, we can do it in windows and Mac cmd 
# but htis just saves time and also it checks the type of variables, did we put something in there and case sensetive 
class Settings(BaseSettings): 
  database_hostname: str
  database_password: str
  database_port: str
  database_name: str
  database_username: str
  secret_key: str 
  algorithm: str
  access_token_expire_minutes: int
  class Config: 
    env_file = ".env"

settings=Settings()