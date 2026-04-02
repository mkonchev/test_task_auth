from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, engine, SessionLocal, Base
from app.api.auth import authRouter
from app.api.admin import adminRouter
from app.api.mock import mockRouter
from app.services.init_service import InitService


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        init_service = InitService(db)
        await init_service.init_all()

    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(authRouter, tags=["auth"], prefix="/auth")
app.include_router(adminRouter)
app.include_router(mockRouter)


@app.get('/')
async def health_check():
    return {'service': 'works'}


@app.get('/db_health')
async def db_health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed. Error:{e}"
        )
