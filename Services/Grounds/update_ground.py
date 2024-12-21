import base64
from typing import List

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_grounds_table, get_ground_facilities_table, get_ground_equipments_table, \
    get_ground_images_table, get_pitches_table
from Services.Grounds.add_grounds import add_pitches, add_ground_images, add_ground_facilities, add_ground_equipments
from Services.Grounds.models import GroundUpdate, Pitch


async def update_ground(ground_id: int, ground_data: GroundUpdate, db: AsyncSession):
    try:
        grounds_table = await get_grounds_table()
        query = (
            update(grounds_table)
            .where(grounds_table.c.id == ground_id)
            .values(**ground_data.model_dump())
        )
        result = await db.execute(query)
        await db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ground not found")
        return {"message": "Ground updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_facilities(ground_id: int, facilities_data: List[str], db: AsyncSession):
    try:
        ground_facilities_table = await get_ground_facilities_table()
        delete_query = ground_facilities_table.delete().where(ground_facilities_table.c.ground_id == ground_id)
        await db.execute(delete_query)

        # Insert new facilities
        for facility in facilities_data:
            await add_ground_facilities(facility, ground_id=ground_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_equipments(ground_id: int, equipments_data: List[str], db: AsyncSession):
    try:
        ground_equipments_table = await get_ground_equipments_table()
        # Delete existing equipments
        delete_query = ground_equipments_table.delete().where(ground_equipments_table.c.ground_id == ground_id)
        await db.execute(delete_query)

        # Insert new equipments
        for equipment in equipments_data:
            await add_ground_equipments(equipment, ground_id=ground_id, db=db)
        return {"message": "Equipments updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_ground_images(ground_id: int, images_data: List[str], db: AsyncSession):
    try:
        ground_images_table = await get_ground_images_table()
        # Delete existing images
        delete_query = ground_images_table.delete().where(ground_images_table.c.ground_id == ground_id)
        await db.execute(delete_query)

        # Insert new images
        for image in images_data:
            await add_ground_images(image, ground_id=ground_id, db=db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_pitches(ground_id: int, pitches_data: dict, db: AsyncSession):
    try:
        pitches_table = await get_pitches_table()
        # Delete existing pitches
        delete_query = pitches_table.delete().where(pitches_table.c.ground_id == ground_id)
        await db.execute(delete_query)

        # Insert new pitches
        for pitch in pitches_data:
            pitch = Pitch(**pitch)
            await add_pitches(pitch_response=pitch, ground_id=ground_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
