from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.business_element import BusinessElement


class BusinessElementRepo(BaseRepository):
    async def get_by_name(self, name: str) -> BusinessElement | None:
        query = select(BusinessElement).where(BusinessElement.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_or_create(self, name: str) -> BusinessElement:
        element = await self.get_by_name(name)
        if not element:
            element = BusinessElement(name=name)
            self.db.add(element)
            await self.db.commit()
            await self.db.refresh(element)
        return element

    async def get_all(self) -> list[BusinessElement]:
        query = select(BusinessElement)
        result = await self.db.execute(query)
        return result.scalars().all()
