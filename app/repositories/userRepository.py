from sqlalchemy import select, update
from app.repositories.base import BaseRepository
from app.models.user import User
from app.models.role import Role
# from app.schemas import user as user_schema


class UserRepo(BaseRepository):
    async def create_user(self, user_data: dict) -> User:
        db_user = User(**user_data)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def create_user_with_role(self, user_data: dict, role: Role) -> User:
        db_user = User(**user_data)

        db_user.roles = [role]
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_user(
        self,
        user_id: int,
        update_data: dict
    ) -> User | None:
        query = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
            .returning(User)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> User | None:
        query = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
            .returning(User)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()
