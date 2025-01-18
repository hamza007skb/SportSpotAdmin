from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.GetBookings.get_bookings import get_user_bookings, get_ground_bookings

router = APIRouter(
    prefix="/show_bookings",
    tags=["show_bookings"],
)


@router.get("/user/{email}")
async def get_user_bookings_router(email: str, db: AsyncSession = Depends(get_db)):
    return await get_user_bookings(user_email=email, session=db)


@router.get("/user/{id}")
async def get_owner_bookings_router(id: int, db: AsyncSession = Depends(get_db)):
    return await get_ground_bookings(ground_id=id, session=db)
