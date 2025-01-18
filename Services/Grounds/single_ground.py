from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_pitches_table, get_user_reviews_table, get_ground_facilities_table, \
    get_ground_equipments_table


class PitchResponseModel(BaseModel):
    ground_id: int
    name: str
    description: str
    length: str
    width: str
    game_type: str
    price_per_60mins: str
    price_per_90mins: str
    created_at: datetime


async def get_pitches(ground_id: int, db: AsyncSession) -> List[PitchResponseModel]:
    pitch_table = await get_pitches_table()
    query = select(pitch_table).where(pitch_table.c.ground_id == int(ground_id))
    result = await db.execute(query)
    rows = result.mappings().all()
    pitches = [PitchResponseModel(**row) for row in rows]

    return pitches


async def get_reviews_by_ground(ground_id: int, db: AsyncSession):
    user_reviews = await get_user_reviews_table()

    # Query to fetch reviews for the specified ground_id
    query = select(user_reviews).where(user_reviews.c.ground_id == ground_id)
    result = await db.execute(query)
    reviews = result.fetchall()

    # If no reviews are found, raise a 404 error
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews found for ground ID {ground_id}")

    # Format and return the results
    return [
        {
            "user_id": review.user_id,
            "rating": review.rating,
            "ground_id": review.ground_id,
            "comment": review.comment,
        }
        for review in reviews
    ]


async def get_facilities_by_ground(ground_id: int, db: AsyncSession):
    try:
        ground_facilities_table = await get_ground_facilities_table()

        # Query to fetch facilities for the specified ground_id
        query = select(ground_facilities_table.c.facility).where(
            ground_facilities_table.c.ground_id == ground_id
        )
        result = await db.execute(query)
        facilities = result.fetchall()

        # If no facilities are found, raise a 404 error
        if not facilities:
            raise HTTPException(
                status_code=404,
                detail=f"No facilities found for ground ID {ground_id}",
            )

        # Format and return the results
        return [facility.facility for facility in facilities]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching facilities: {e}"
        )


async def get_equipments_by_ground(ground_id: int, db: AsyncSession):
    try:
        ground_equipments_table = await get_ground_equipments_table()

        # Query to fetch equipment for the specified ground_id
        query = select(ground_equipments_table.c.equipment).where(
            ground_equipments_table.c.ground_id == ground_id
        )
        result = await db.execute(query)
        equipments = result.fetchall()

        # If no equipment is found, raise a 404 error
        if not equipments:
            raise HTTPException(
                status_code=404,
                detail=f"No equipment found for ground ID {ground_id}",
            )

        # Format and return the results
        return [equipment.equipment for equipment in equipments]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching equipment: {e}"
        )

