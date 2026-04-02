from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.models.business_element import BusinessElement
from app.models.access_rule import AccessRule
from app.models.user import User
from app.security.hashHelper import HashHelper
from app.db.config import settings


class InitService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def init_roles(self):
        """Создание ролей по умолчанию"""
        roles_data = ["admin", "manager", "user", "guest"]

        roles = {}
        for role_name in roles_data:
            result = await self.db.execute(
                select(Role).where(Role.name == role_name)
            )
            role = result.scalar_one_or_none()
            if not role:
                role = Role(name=role_name)
                self.db.add(role)
                await self.db.flush()
            roles[role_name] = role

        await self.db.commit()
        for role in roles.values():
            await self.db.refresh(role)
        return roles

    async def init_business_elements(self):
        """Создание business_elements по умолчанию"""
        elements_data = [
            "users",
            "access_rules",
            "mock_data"
        ]

        elements = {}
        for element_name in elements_data:
            result = await self.db.execute(
                select(BusinessElement)
                .where(BusinessElement.name == element_name)
            )
            element = result.scalar_one_or_none()
            if not element:
                element = BusinessElement(name=element_name)
                self.db.add(element)
                await self.db.flush()
            elements[element_name] = element

        await self.db.commit()
        for element in elements.values():
            await self.db.refresh(element)
        return elements

    async def init_access_rules(self, roles: dict, elements: dict):
        """Создание правил доступа"""

        admin_rules = {
            "users": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": True,
                "update_permission": True, "update_all_permission": True,
                "delete_permission": True, "delete_all_permission": True,
            },
            "access_rules": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": True,
                "update_permission": True, "update_all_permission": True,
                "delete_permission": True, "delete_all_permission": True,
            },
            "mock_data": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": True,
                "update_permission": True, "update_all_permission": True,
                "delete_permission": True, "delete_all_permission": True,
            },
        }

        manager_rules = {
            "users": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": True,
                "update_permission": True, "update_all_permission": False,
                "delete_permission": True, "delete_all_permission": False,
            },
            "access_rules": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": False,
                "update_permission": False, "update_all_permission": False,
                "delete_permission": False, "delete_all_permission": False,
            },
            "mock_data": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": True,
                "update_permission": True, "update_all_permission": False,
                "delete_permission": True, "delete_all_permission": False,
            },
        }

        user_rules = {
            "users": {
                "read_permission": True, "read_all_permission": False,
                "create_permission": False,
                "update_permission": True, "update_all_permission": False,
                "delete_permission": True, "delete_all_permission": False,
            },
            "access_rules": {
                "read_permission": False, "read_all_permission": False,
                "create_permission": False,
                "update_permission": False, "update_all_permission": False,
                "delete_permission": False, "delete_all_permission": False,
            },
            "mock_data": {
                "read_permission": True, "read_all_permission": False,
                "create_permission": True,
                "update_permission": True, "update_all_permission": False,
                "delete_permission": True, "delete_all_permission": False,
            },
        }

        guest_rules = {
            "users": {
                "read_permission": False, "read_all_permission": False,
                "create_permission": False,
                "update_permission": False, "update_all_permission": False,
                "delete_permission": False, "delete_all_permission": False,
            },
            "access_rules": {
                "read_permission": False, "read_all_permission": False,
                "create_permission": False,
                "update_permission": False, "update_all_permission": False,
                "delete_permission": False, "delete_all_permission": False,
            },
            "mock_data": {
                "read_permission": True, "read_all_permission": True,
                "create_permission": False,
                "update_permission": False, "update_all_permission": False,
                "delete_permission": False, "delete_all_permission": False,
            },
        }

        role_rules = {
            "admin": admin_rules,
            "manager": manager_rules,
            "user": user_rules,
            "guest": guest_rules,
        }

        for role_name, rules in role_rules.items():
            role = roles.get(role_name)
            if not role:
                continue

            for element_name, permissions in rules.items():
                element = elements.get(element_name)
                if not element:
                    continue

                result = await self.db.execute(
                    select(AccessRule).where(
                        AccessRule.role_id == role.id,
                        AccessRule.element_id == element.id
                    )
                )
                rule = result.scalar_one_or_none()

                if not rule:
                    rule = AccessRule(
                        role_id=role.id,
                        element_id=element.id,
                        **permissions
                    )
                    self.db.add(rule)
                else:
                    for key, value in permissions.items():
                        setattr(rule, key, value)
        await self.db.commit()

    async def create_test_admin(self, roles: dict):
        result = await self.db.execute(select(User).limit(1))
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            admin_role = roles.get("admin")
            if admin_role:
                await self.db.refresh(admin_role)

                admin_user = User(
                    first_name="Admin",
                    last_name="User",
                    email=settings.ADMIN_EMAIL,
                    password=await HashHelper.get_password_hash(
                        settings.ADMIN_PW
                    ),
                    is_active=True,
                    roles=[admin_role]
                )
                self.db.add(admin_user)
                await self.db.commit()

    async def init_all(self):
        """Инициализация всех данных"""

        roles = await self.init_roles()

        elements = await self.init_business_elements()

        await self.init_access_rules(roles, elements)

        await self.create_test_admin(roles)
