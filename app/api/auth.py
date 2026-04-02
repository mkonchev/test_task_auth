from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import user as user_schema
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.services.user_service import UserService
from app.models.user import User


authRouter = APIRouter()


@authRouter.post(
    "/register",
    response_model=user_schema.UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: user_schema.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        user_service = UserService(db)
        user = await user_service.register(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@authRouter.post(
    "/login",
    response_model=user_schema.UserToken,
    status_code=status.HTTP_200_OK
)
async def login(
    user_data: user_schema.UserLogin,
    db: AsyncSession = Depends(get_db)
):
    try:
        user_service = UserService(db)
        token = await user_service.login(user_data)
        return user_schema.UserToken(token=token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@authRouter.post("/logout")
async def logout():
    return {"data": "success"}


@authRouter.patch(
    "/update",
    response_model=user_schema.UserResponse,
    status_code=status.HTTP_200_OK
)
async def update(
    update_data: user_schema.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        user_service = UserService(db)
        updated_user = await (
            user_service.update_user(current_user.id, update_data)
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@authRouter.patch("/delete")
async def delete(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        user_service = UserService(db)
        await user_service.delete_user(current_user.id)
        return {"message": "User deactivated"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
