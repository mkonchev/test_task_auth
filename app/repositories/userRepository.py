from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.user import User
# from app.schemas import user as user_schema


class UserRepo(BaseRepository):
    async def create_user(self, user_data: dict) -> User:
        db_user = User(**user_data)

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

