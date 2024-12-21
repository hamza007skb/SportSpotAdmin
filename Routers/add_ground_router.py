from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.Grounds.add_grounds import add_ground_details

router = APIRouter(
    prefix="/add_ground",
    tags=["Add Ground"],
)

@router.post("/ground")
async def add_ground(ground_response: dict, db: AsyncSession = Depends(get_db)):
    return await add_ground_details(response=ground_response, db=db)

