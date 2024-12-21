from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Async_DB_Connection import get_db
from Services.Overview.stats import get_stats

router = APIRouter(
    prefix="/stats",
    tags=["Stats Overview"],
)

@router.get('/overview')
async def get_overview(db: AsyncSession = Depends(get_db)):
    return await get_stats(db=db)
