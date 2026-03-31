from fastapi import APIRouter
from app.schemas import user as user_schema

authRouter = APIRouter()


@authRouter.post("/register")
async def register(user_data: user_schema.UserCreate):
    return {"data": user_schema.UserResponse}


@authRouter.post("/login")
async def login(user_data: user_schema.UserLogin):
    return {"data": f"User {user_data.email} login successfully"}


@authRouter.post("/logout")
async def logout():
    return {"data": "success"}


@authRouter.patch("/update")
async def update():
    return {"data": "success"}


@authRouter.patch("/delete")
async def delete():
    return {"data": "success"}
