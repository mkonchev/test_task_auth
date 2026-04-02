from sqlalchemy import select, update, delete
from app.repositories.base import BaseRepository
from app.models.access_rule import AccessRule


class AccessRuleRepo(BaseRepository):
    async def get_by_role_and_element(
        self, role_id: int, element_id: int
    ) -> AccessRule | None:
        query = select(AccessRule).where(
            AccessRule.role_id == role_id,
            AccessRule.element_id == element_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, rule_id: int) -> AccessRule | None:
        """Получить правило по ID"""
        query = select(AccessRule).where(AccessRule.id == rule_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[AccessRule]:
        query = select(AccessRule)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_rules_by_role(self, role_id: int) -> list[AccessRule]:
        query = select(AccessRule).where(AccessRule.role_id == role_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_rule(self, rule_data: dict) -> AccessRule:
        rule = AccessRule(**rule_data)
        self.db.add(rule)
        await self.db.commit()
        await self.db.refresh(rule)
        return rule

    async def update_rule(
        self, rule_id: int, update_data: dict
    ) -> AccessRule | None:
        query = (
            update(AccessRule)
            .where(AccessRule.id == rule_id)
            .values(**update_data)
            .returning(AccessRule)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_rule(self, rule_id: int) -> bool:
        query = delete(AccessRule).where(AccessRule.id == rule_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
