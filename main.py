from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
AlgORITHM = os.getenv("ALGORITHM")
Access_TOKEN_EXPIRE_MINUTES= int(os.getenv("Access_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Oath2_schema= OAuth2PasswordBearer(tokenUrl="auth/Login.form")
from auth_routes import auth_router
from order_routes import order_router
app.include_router(auth_router)
app.include_router(order_router)

