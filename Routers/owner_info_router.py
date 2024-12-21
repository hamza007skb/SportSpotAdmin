from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.GetOwners.owners import get_all_owners

router = APIRouter(
    prefix="/owners",
    tags=["Owners Info"],
)

@router.get("/read")
async def read_owners_info(db: AsyncSession = Depends(get_db)):
    return await get_all_owners(db=db)