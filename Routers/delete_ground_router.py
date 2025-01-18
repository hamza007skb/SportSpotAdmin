from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.Grounds.delete_ground import delete_ground

router = APIRouter(
    prefix="/delete_ground",
    tags=["Delete Ground"],
)


@router.delete('/{id}')
async def delete_ground_router(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_ground(id, db)
