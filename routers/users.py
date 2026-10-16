from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status
from models import Todos, Users
from database import SessionLocal
from .auth import get_current_user
import bcrypt

router = APIRouter(
    prefix="/users",
    tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=5, max_length=64)

@router.get("/")
async def get_current_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    return user_model

@router.put("/password", status_code=status.HTTP_201_CREATED)
async def change_password(user: user_dependency,
                          user_verification: UserVerification,
                          db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt.checkpw(user_verification.password.encode("utf-8"), user_model.hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail='Incorrect password.')
    new_hashed_password = (bcrypt
                           .hashpw(user_verification.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    user_model.hashed_password = new_hashed_password
    db.add(user_model)
    db.commit()
