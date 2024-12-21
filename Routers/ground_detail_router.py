from select import select
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Database.async_tables import get_grounds_table, get_ground_images_table
from Services.Grounds.single_ground import get_pitches, get_reviews_by_ground, get_facilities_by_ground, \
    get_equipments_by_ground

router = APIRouter(
    prefix="/ground_detail",
    tags=["Ground Detail"],
)


@router.get("/ground/{id}", response_model=Dict)
async def get_ground_details(id: int, db: AsyncSession = Depends(get_db)):
    grounds_table = await get_grounds_table()
    ground_query = select(grounds_table).where(grounds_table.c.id == int(id))
    ground = await db.execute(ground_query)
    ground_data = ground.scalar_one_or_none()

    if not ground_data:
        raise HTTPException(status_code=404, detail="Ground not found")
    return ground_data

@router.get("/ground_imgs/{id}")
async def get_ground_details(id: int, db: AsyncSession = Depends(get_db)):
    ground_imgs_table = await get_ground_images_table()
    ground_query = select(ground_imgs_table).where(ground_imgs_table.c.id == int(id))
    ground = await db.execute(ground_query)
    ground_data = ground.scalar_one_or_none()

    if not ground_data:
        raise HTTPException(status_code=404, detail="Ground not found")
    return ground_data

@router.get("/pitches/{ground_id}")
async def get_ground_pitches(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_pitches(ground_id=ground_id, db=db)

@router.get("/reviews/{ground_id}")
async def get_ground_reviews(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_reviews_by_ground(ground_id=ground_id, db=db)


@router.get("/facilities/{ground_id}")
async def get_ground_facilities(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_facilities_by_ground(ground_id=ground_id, db=db)


@router.get("/equipment/{ground_id}")
async def get_ground_equipment(ground_id: int, db: AsyncSession = Depends(get_db)):
    return await get_equipments_by_ground(ground_id=ground_id, db=db)