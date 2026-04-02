from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
# from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import require_permission
from app.api.auth import get_current_user
from app.services.permission_service import Action
from app.models.user import User

mockRouter = APIRouter(prefix="/mock", tags=["mock"])


class Article(BaseModel):
    id: int
    title: str
    content: str
    user_id: int | None
    created_at: datetime = datetime.now()


mock_articles = [
    Article(id=1, title="My First Article", content="Content 1", user_id=1),
    Article(id=2, title="Admin Post", content="Content 2", user_id=1),
    Article(id=3, title="Manager Note", content="Content 3", user_id=2),
]


async def get_article_owner(
    article_id: int, user: User, db=None
) -> Optional[int]:
    article = next((a for a in mock_articles if a.id == article_id), None)
    return article.user_id if article else None


async def check_article_permission(
    article_id: int = Path(...),
    current_user: User = Depends(get_current_user)
) -> User:
    owner_id = await get_article_owner(article_id)
    if owner_id is None:
        raise HTTPException(status_code=404, detail="Article not found")

    permission_dep = require_permission(
        "mock_data", Action.UPDATE, resource_owner_id=owner_id
    )
    return await permission_dep(current_user)


@mockRouter.get("/articles", response_model=List[Article])
async def get_all_articles(
    _=Depends(require_permission("mock_data", Action.READ_ALL))
):
    return mock_articles


@mockRouter.get("/articles/my", response_model=List[Article])
async def get_my_articles(
    current_user: User = Depends(get_current_user),
    _=Depends(require_permission("mock_data", Action.READ))
):
    user_articles = [a for a in mock_articles if a.user_id == current_user.id]
    return user_articles


@mockRouter.post("/articles", response_model=Article, status_code=201)
async def create_article(
    title: str,
    content: str,
    current_user: User = Depends(
        require_permission("mock_data", Action.CREATE)
    )
):
    new_id = len(mock_articles) + 1
    article = Article(
        id=new_id,
        title=title,
        content=content,
        user_id=current_user.id
    )
    mock_articles.append(article)
    return article


@mockRouter.put("/articles/{article_id}", response_model=Article)
async def update_article(
    article_id: int,
    title: str,
    content: str,
    current_user: User = Depends(check_article_permission)
):
    article = next((a for a in mock_articles if a.id == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.title = title
    article.content = content
    return article


@mockRouter.delete("/articles/{article_id}")
async def delete_article(
    article_id: int,
    current_user: User = Depends(check_article_permission)
):
    article = next((a for a in mock_articles if a.id == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    mock_articles.remove(article)
    return {"message": "Article deleted successfully"}
