from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.Grounds.models import GroundUpdate
from Services.Grounds.update_ground import update_ground, update_facilities, update_equipments, update_pitches, \
    update_ground_images

router = APIRouter(
    prefix="/update_ground",
    tags=["Ground Update"],
)


@router.post("/ground/{id}")
async def ground_update(id: int, ground: dict, db: AsyncSession = Depends(get_db)):
    try:
        ground = GroundUpdate(**ground)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    await update_ground(ground_id=id, ground_data=ground, db=db)


@router.post("/facilities/{id}")
async def ground_facilities_update(id: int, facilities: List[str], db: AsyncSession = Depends(get_db)):
    await update_facilities(ground_id=id, facilities_data=facilities, db=db)


@router.post("/equipment/{id}")
async def ground_equipments_update(id: int, equipments: List[str], db: AsyncSession = Depends(get_db)):
    await update_equipments(ground_id=id, equipments_data=equipments, db=db)


@router.post("/pitches/{id}")
async def pitches_update(ground_id: int, pitches_data: dict, db: AsyncSession = Depends(get_db)):
    await update_pitches(ground_id=ground_id, pitches_data=pitches_data, db=db)


@router.post("/images/{id}")
async def images_update(ground_id: int, images_data: List[str], db: AsyncSession = Depends(get_db)):
    await update_ground_images(ground_id=ground_id, images_data=images_data, db=db)
