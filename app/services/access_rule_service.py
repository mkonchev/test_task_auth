from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.acces_rule_repository import AccessRuleRepo
from app.repositories.role_repository import RoleRepo
from app.repositories.buseness_element_repository import BusinessElementRepo
from app.schemas import access_rule as rule_schema


class AccessRuleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.access_rule_repo = AccessRuleRepo(db)
        self.role_repo = RoleRepo(db)
        self.element_repo = BusinessElementRepo(db)

    async def get_all_rules(self):
        """Получить все правила доступа"""
        return await self.access_rule_repo.get_all()

    async def get_rule_by_id(self, rule_id: int):
        """Получить правило по ID"""
        rule = await self.access_rule_repo.get_by_id(rule_id)
        if not rule:
            raise ValueError("Rule not found")
        return rule

    async def create_rule(self, rule_data: rule_schema.AccessRuleCreate):
        role = await self.role_repo.get_by_id(rule_data.role_id)
        if not role:
            raise ValueError("Role not found")

        element = await self.element_repo.get_by_id(rule_data.element_id)
        if not element:
            raise ValueError("Business element not found")

        existing = await self.access_rule_repo.get_by_role_and_element(
            rule_data.role_id, rule_data.element_id
        )
        if existing:
            raise ValueError("Rule already exists for this role and element")

        return await self.access_rule_repo.create_rule(rule_data.model_dump())

    async def update_rule(
        self,
        rule_id: int,
        rule_data: rule_schema.AccessRuleUpdate
    ):
        existing = await self.access_rule_repo.get_by_id(rule_id)
        if not existing:
            raise ValueError("Rule not found")

        updated = await self.access_rule_repo.update_rule(
            rule_id, rule_data.model_dump(exclude_none=True)
        )
        if not updated:
            raise ValueError("Failed to update rule")

        return updated

    async def delete_rule(self, rule_id: int):
        existing = await self.access_rule_repo.get_by_id(rule_id)
        if not existing:
            raise ValueError("Rule not found")

        deleted = await self.access_rule_repo.delete_rule(rule_id)
        if not deleted:
            raise ValueError("Failed to delete rule")

        return {"message": "Rule deleted successfully"}
