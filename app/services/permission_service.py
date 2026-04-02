# app/services/permission_service.py
from enum import Enum
from app.models.user import User
from app.repositories.acces_rule_repository import AccessRuleRepo
from app.repositories.buseness_element_repository import BusinessElementRepo


class Action(str, Enum):
    READ = "read"
    READ_ALL = "read_all"
    CREATE = "create"
    UPDATE = "update"
    UPDATE_ALL = "update_all"
    DELETE = "delete"
    DELETE_ALL = "delete_all"


class PermissionService:
    def __init__(self, db):
        self.db = db
        self.access_rule_repo = AccessRuleRepo(db)
        self.business_element_repo = BusinessElementRepo(db)

    async def check_permission(
        self,
        user: User,
        element_name: str,
        action: Action,
        resource_owner_id: int | None = None
    ) -> bool:
        element = await self.business_element_repo.get_by_name(element_name)
        if not element:
            return False

        for role in user.roles:
            rule = await self.access_rule_repo.get_by_role_and_element(
                role.id,
                element.id
            )
            if not rule:
                continue

            if action == Action.READ:
                if resource_owner_id:
                    if rule.read_all_permission or (
                        rule.read_permission and resource_owner_id == user.id
                    ):
                        return True
                else:
                    if rule.read_all_permission or rule.read_permission:
                        return True

            elif action == Action.READ_ALL:
                if rule.read_all_permission:
                    return True

            elif action == Action.CREATE:
                if rule.create_permission:
                    return True

            elif action == Action.UPDATE:
                if resource_owner_id:
                    if rule.update_all_permission or (
                        rule.update_permission and resource_owner_id == user.id
                    ):
                        return True
                else:
                    if rule.update_all_permission or rule.update_permission:
                        return True

            elif action == Action.UPDATE_ALL:
                if rule.update_all_permission:
                    return True

            elif action == Action.DELETE:
                if resource_owner_id:
                    if rule.delete_all_permission or (
                        rule.delete_permission and resource_owner_id == user.id
                    ):
                        return True
                else:
                    if rule.delete_all_permission or rule.delete_permission:
                        return True

            elif action == Action.DELETE_ALL:
                if rule.delete_all_permission:
                    return True

        return False
