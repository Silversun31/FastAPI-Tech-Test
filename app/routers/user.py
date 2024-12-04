from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, views, models
from app.database import get_db
from app.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/register", response_model=schemas.User, tags=["Auth"], status_code=201)
async def register_user(user: schemas.UserCreate, db_session: AsyncSession = Depends(get_db)):
    async with db_session as db:
        db_user = await views.user.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return await views.user.create_user(db=db, user=user)


@router.post("/login", tags=["Auth"])
async def login_user(username: str = Form(None), password: str = Form(None),
                     db_session: AsyncSession = Depends(get_db)):
    async with db_session as db:
        db_user = await views.user.get_user_by_username(db, username=username)
        if not db_user or not verify_password(password, db_user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        access_token = create_access_token(data={"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer"}
