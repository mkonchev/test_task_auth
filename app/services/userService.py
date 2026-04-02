from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.userRepository import UserRepo
from app.repositories.roleRepository import RoleRepo
from app.schemas import user as user_schema
from app.security.authHandler import AuthHandler
from app.security.hashHelper import HashHelper


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.__userRepository = UserRepo(db=db)
        self.__roleRepository = RoleRepo(db=db)

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
        default_role = await self.__roleRepository.get_or_create("user")

        user_dict = user_data.model_dump(exclude={'repeat_password'})

        hashed_password = await (
            HashHelper.get_password_hash(user_data.password)
        )
        user_dict['password'] = hashed_password

        user = await self.__userRepository.create_user_with_role(
            user_dict,
            default_role
        )

        return user_schema.UserResponse.model_validate(user)

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

    async def get_user_by_id(self, user_id: int):
        return await self.__userRepository.get_user_by_id(user_id)

    async def delete_user(self, user_id: int) -> None:
        user = await self.__userRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.is_active = False
        await self.__userRepository.update_user(user)

    async def update_user(
        self,
        user_id: int,
        update_data: user_schema.UserUpdate
    ) -> user_schema.UserResponse:
        user = await self.__userRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError(
                "No such user"
            )

        update_user_dict = update_data.model_dump(
            exclude_none=True,
            exclude={'repeat_password'}
        )

        if 'password' in update_user_dict:
            update_user_dict['password'] = await (
                HashHelper.get_password_hash(update_user_dict['password'])
            )

        updated_user = await (
            self.__userRepository.update_user(user_id, update_user_dict)
        )

        return user_schema.UserResponse.model_validate(updated_user)
