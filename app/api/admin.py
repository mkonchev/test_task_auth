from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.dependencies import require_permission
from app.services.permission_service import Action
from app.services.access_rule_service import AccessRuleService
from app.schemas import access_rule as rule_schema

adminRouter = APIRouter(prefix="/admin", tags=["admin"])


@adminRouter.get("/access-rules")
async def get_all_rules(
    _=Depends(require_permission("access_rules", Action.READ_ALL)),
    db: AsyncSession = Depends(get_db)
):
    try:
        service = AccessRuleService(db)
        rules = await service.get_all_rules()
        return rules
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@adminRouter.get("/access-rules/{rule_id}")
async def get_rule(
    rule_id: int,
    _=Depends(require_permission("access_rules", Action.READ_ALL)),
    db: AsyncSession = Depends(get_db)
):
    try:
        service = AccessRuleService(db)
        rule = await service.get_rule_by_id(rule_id)
        return rule
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@adminRouter.post("/access-rules", status_code=status.HTTP_201_CREATED)
async def create_rule(
    rule_data: rule_schema.AccessRuleCreate,
    _=Depends(require_permission("access_rules", Action.CREATE)),
    db: AsyncSession = Depends(get_db)
):
    try:
        service = AccessRuleService(db)
        rule = await service.create_rule(rule_data)
        return rule
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@adminRouter.put("/access-rules/{rule_id}")
async def update_rule(
    rule_id: int,
    rule_data: rule_schema.AccessRuleUpdate,
    _=Depends(require_permission("access_rules", Action.UPDATE_ALL)),
    db: AsyncSession = Depends(get_db)
):
    try:
        service = AccessRuleService(db)
        rule = await service.update_rule(rule_id, rule_data)
        return rule
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@adminRouter.delete("/access-rules/{rule_id}")
async def delete_rule(
    rule_id: int,
    _=Depends(require_permission("access_rules", Action.DELETE_ALL)),
    db: AsyncSession = Depends(get_db)
):
    try:
        service = AccessRuleService(db)
        result = await service.delete_rule(rule_id)
        return result
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
