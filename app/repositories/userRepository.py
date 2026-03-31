from app.repositories.base import BaseRepository
from app.models.user import User
from app.schemas import user as user_schema


class UserRepo(BaseRepository):
    async def create_user(self, user_data: user_schema.UserCreate) -> User:
        db_user = User(user_data.model_dump(exclude_none=True))

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    async def get_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter_by(email=email).first()
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter_by(id=user_id).first()
        return user
