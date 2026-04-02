from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.role import Role


class RoleRepo(BaseRepository):
    async def get_by_name(self, name: str) -> Role | None:
        query = select(Role).where(Role.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_or_create(self, name: str) -> Role:
        role = await self.get_by_name(name)
        if not role:
            role = Role(name=name)
            self.db.add(role)
            await self.db.commit()
            await self.db.refresh(role)
        return role

    async def get_by_id(self, role_id: int) -> Role | None:
        query = select(Role).where(Role.id == role_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Role]:
        query = select(Role)
        result = await self.db.execute(query)
        return result.scalars().all()
