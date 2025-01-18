from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.DeleteOwner.delete_owner import delete_owner
from Services.DeleteUser.delete_user import delete_user

router = APIRouter(
    prefix="/delete_user",
    tags=["Delete User"],
)

@router.delete("/owner/{email}", status_code=204)
async def delete_owner_router(email: str, db: AsyncSession = Depends(get_db)):
    return await delete_owner(email=email, db=db)

@router.delete("/user/{email}", status_code=204)
async def delete_user_router(email: str, db: AsyncSession = Depends(get_db)):
    return await delete_user(email=email, db=db)