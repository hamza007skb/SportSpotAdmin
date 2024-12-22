from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_grounds_table, get_ground_facilities_table, get_ground_equipments_table, \
    get_ground_images_table, get_pitches_table, get_bookings_table, get_ground_owners_table, get_user_reviews_table


async def delete_ground(ground_id: int, db: AsyncSession):
    try:
        await delete_ground_owners(ground_id, db)
        await delete_ground_reviews(ground_id=ground_id, db=db)
        await delete_ground_bookings(ground_id, db)
        await delete_facilities(ground_id, db)
        await delete_equipments(ground_id, db)
        await delete_pitches(ground_id, db)
        await delete_ground_images(ground_id, db)

        grounds_table = await get_grounds_table()
        query = grounds_table.delete().where(grounds_table.c.id == ground_id)
        await db.execute(query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_facilities(ground_id: int, db: AsyncSession):
    try:
        ground_facilities_table = await get_ground_facilities_table()
        delete_query = ground_facilities_table.delete().where(ground_facilities_table.c.ground_id == ground_id)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_equipments(ground_id: int, db: AsyncSession):
    try:
        ground_equipments_table = await get_ground_equipments_table()
        # Delete existing equipments
        delete_query = ground_equipments_table.delete().where(ground_equipments_table.c.ground_id == ground_id)
        await db.execute(delete_query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_ground_images(ground_id: int, db: AsyncSession):
    try:
        ground_images_table = await get_ground_images_table()
        delete_query = ground_images_table.delete().where(ground_images_table.c.ground_id == ground_id)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_pitches(ground_id: int, db: AsyncSession):
    try:
        pitches_table = await get_pitches_table()
        # Delete existing pitches
        delete_query = pitches_table.delete().where(pitches_table.c.ground_id == ground_id)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_ground_bookings(ground_id: int, db: AsyncSession):
    try:
        bookings_table = await get_bookings_table()
        # Delete existing pitches
        delete_query = bookings_table.delete().where(bookings_table.c.ground_id == ground_id)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_ground_owners(ground_id: int, db: AsyncSession):
    try:
        ground_owners = await get_ground_owners_table()
        # Delete existing pitches
        delete_query = ground_owners.delete().where(ground_owners.c.ground_id == ground_id)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_ground_reviews(ground_id: int, db: AsyncSession):
    try:
        reviews = await get_user_reviews_table()
        # Delete existing pitches
        delete_query = reviews.delete().where(reviews.c.ground_id == ground_id)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))