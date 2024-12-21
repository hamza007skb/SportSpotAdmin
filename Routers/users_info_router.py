from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.GetUsers.users import get_all_users

router = APIRouter(
    prefix="/users",
    tags=["Users Info"],
)

@router.get("/read")
async def read_users_info(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db=db)
