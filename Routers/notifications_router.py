from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Async_DB_Connection import get_db
from Services.Notifications.notifications import get_notifications, read_notification, mark_all_notifications_as_read, \
    get_single_notification

router = APIRouter(
    prefix="/notifications",
    tags=["Admin Notifications"],
)


@router.get("/messages")
async def get_notification_list(db: AsyncSession = Depends(get_db)):
    return await get_notifications(db=db)


@router.post("/update_read/{id}")
async def update_read(id: int, db: AsyncSession = Depends(get_db)):
    return await read_notification(notification_id=id, db=db)


@router.post("/read_all")
async def read_all_notifications(db: AsyncSession = Depends(get_db)):
    return await mark_all_notifications_as_read(db=db)


@router.get("/msg/{id}")
async def get_message(id: int, db: AsyncSession = Depends(get_db)):
    return await get_single_notification(notification_id=id, db=db)
