import base64
import logging
from typing import List

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from Database.async_tables import get_owners_table, get_grounds_table, get_ground_owners_table, \
    get_ground_facilities_table, get_ground_equipments_table, get_pitches_table, get_ground_images_table
from Services.Grounds.models import GroundDetails, Pitch

async def add_ground_details(response: dict, db: AsyncSession):
    try:
        for key, value in response.items():
            if key != 'images':
                print(key, value)
        ground_details = response.get('ground')
        owner_email = response.get('ownerEmail')
        pitches_detail = response.get('pitches')
        equipments_detail = response.get('equipments', [])
        facility_details = response.get('facilities', [])
        image_details = response.get('images')

        if 'latitude' in ground_details:
            ground_details['latitude'] = str(ground_details['latitude'])
        if 'longitude' in ground_details:
            ground_details['longitude'] = str(ground_details['longitude'])

        ground_details['email'] = owner_email       ##owner email is ground email
        # Create ground entry
        ground = GroundDetails(**ground_details)
        ground_id = await add_ground(ground_response=ground, owner_email=owner_email, db=db)

        if not ground_id:
            return {'response': '404 Ground Not Found'}

        # Insert pitches if ground is created successfully
        for pitch in pitches_detail:
            pitch = Pitch(**pitch)
            await add_pitches(pitch_response=pitch, ground_id=ground_id, db=db)

        for equipment in equipments_detail:
            await add_ground_equipments(equipment, ground_id=ground_id, db=db)
        for facility in facility_details:
            await add_ground_facilities(facility, ground_id=ground_id, db=db)
        for image in image_details:
            if image != 'Add photo':
                await add_ground_images(image, ground_id=ground_id, db=db)

        return {'id': ground_id, 'response': '200 OK'}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))




async def add_ground(ground_response: GroundDetails, owner_email: str, db: AsyncSession) -> int:

    ground_data = ground_response.model_dump()
    try:
        ground_table = await get_grounds_table()
        ground_owners_table = await get_ground_owners_table()
        query1 = insert(ground_table).values(**ground_data).returning(ground_table.c.id)
        result = await db.execute(query1)
        ground_id = result.scalar()
        await db.commit()
        query2 = insert(ground_owners_table).values(ground_id=ground_id, owner_email=owner_email)
        await db.execute(query2)
        await db.commit()

        return ground_id
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def add_pitches(pitch_response: Pitch, ground_id: int, db: AsyncSession):
    pitches_data = pitch_response.model_dump()
    pitches_data['ground_id'] = ground_id
    # if pitches_data['pitchName'] in pitches_data.keys():
    #     pitches_data['name'] = pitches_data['pitchName']
    #     del pitches_data['pitchName']
    # if pitches_data['pitchDescription'] in pitches_data.keys():
    #     pitches_data['description'] = pitches_data['pitchDescription']
    #     del pitches_data['pitchDescription']
    logger = logging.getLogger(__name__)
    # logger.error("add_pitches")
    # logger.error(pitches_data)
    try:
        pitches_table = await get_pitches_table()
        query = insert(pitches_table).values(**pitches_data)
        await db.execute(query)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def add_ground_equipments(equipment: str, ground_id: int, db: AsyncSession):
    try:
        equipment_table = await get_ground_equipments_table()
        query = insert(equipment_table).values(equipment=equipment, ground_id=ground_id)
        await db.execute(query)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def add_ground_facilities(facility: str, ground_id: int, db: AsyncSession):
    try:
        facilities_table = await get_ground_facilities_table()
        query = insert(facilities_table).values(facility=facility, ground_id=ground_id)
        await db.execute(query)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


from sqlalchemy import insert
import base64

async def add_ground_images(image: str, ground_id: int, db: AsyncSession):
    try:
        image_data = base64.b64decode(image)
        ground_images_table = await get_ground_images_table()
        query = insert(ground_images_table).values(
            ground_id=ground_id, image_data=image_data
        )
        await db.execute(query)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
