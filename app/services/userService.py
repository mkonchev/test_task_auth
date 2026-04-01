from app.repositories.userRepository import UserRepo
from app.schemas import user as user_schema
from app.security.authHandler import AuthHandler
from app.security.hashHelper import HashHelper
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, db: AsyncSession):
        self.__userRepository = UserRepo(db=db)

    async def register(
        self,
        user_data: user_schema.UserCreate
    ) -> user_schema.UserResponse:
        if await (
            self.__userRepository.get_user_by_email(email=user_data.email)
        ):
            raise ValueError(
                "User with this email already exists"
            )

        user_dict = user_data.model_dump(exclude={'repeat_password'})

        hashed_password = await (
            HashHelper.get_password_hash(user_data.password)
        )
        user_dict['password'] = hashed_password

        return await self.__userRepository.create_user(user_dict)

    async def login(
        self,
        user_data: user_schema.UserLogin
    ) -> user_schema.UserToken:
        user = await self.__userRepository.get_user_by_email(user_data.email)

        if not user:
            raise ValueError(
                "Invalid user data"
            )

        if not user.is_active:
            raise ValueError(
                "User deactivated"
            )

        is_valid = await HashHelper.verify_password(
            user_data.password,
            user.password
        )

        if not is_valid:
            raise ValueError(
                "Invalid password"
            )

        token = await AuthHandler.sign_jwt(user.id)

        return token

    async def delete_user(self, user_id: int) -> None:
        user = await self.__userRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        user.is_active = False
        await self.__userRepository.update_user(user)