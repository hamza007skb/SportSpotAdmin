from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.Grounds.get_grounds import get_grounds_by_owner, get_photos_by_ground, get_all_grounds, get_ground_images, \
    get_all_grounds_with_images
from Services.Grounds.models import GroundResponseModel

router = APIRouter(
    prefix="/ground_list",
    tags=["Ground List"],
)


@router.get("/grounds/{email}")
async def get_ground_list(email: str, db: AsyncSession = Depends(get_db)):
    return await get_grounds_by_owner(owner=email, db=db)


@router.get("/images/{id}")
async def get_ground_list_photos(id: int, db: AsyncSession = Depends(get_db)):
    return await get_photos_by_ground(id, db=db)


@router.get("/grounds")
async def get_all_ground_list(db: AsyncSession = Depends(get_db)):
    # return await get_all_grounds(db=db)
    return await get_all_grounds_with_images(db=db)


@router.get("/groundimages/{images_id}")
async def get_images(images_id: int, db: AsyncSession = Depends(get_db)):
    try:
        images_id = int(images_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid ID format")
    return await get_ground_images(id=images_id, db=db)

