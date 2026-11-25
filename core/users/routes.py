from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from users.schemas import UserLoginSchema, UserRegisterSchema
from users.models import UserModel, TokenModel
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets

router = APIRouter(tags=["users"], prefix="/users")


def generate_token(length=32):
    """Generate a secure random token as a string"""
    return secrets.token_hex(length)


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter(and_(
        UserModel.username == request.username.lower(), UserModel.email == request.email)).first()

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user with this username or email does not found")

    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid password")

    token_obj = TokenModel(user_id=user_obj.id, token=generate_token())
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)

    return JSONResponse(content={"detail": "user logged in successfuly", "token": token_obj.token})


@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(
        or_(
            UserModel.username == request.username.lower(),
            UserModel.email == request.email
        )
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already exists"
        )

    user_obj = UserModel(
        username=request.username.lower(), email=request.email)

    user_obj.set_password(request.password)

    db.add(user_obj)
    db.commit()

    return JSONResponse(content={"detail": "user registered successfully"})
