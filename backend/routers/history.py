from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from schemas.models import TestRun

router = APIRouter(prefix="/history", tags=["history"])

@router.get("")
async def get_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestRun).order_by(TestRun.timestamp.desc()).limit(50))
    runs = result.scalars().all()
    return runs
