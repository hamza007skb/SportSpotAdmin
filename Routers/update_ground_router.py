import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Async_DB_Connection import get_db
from Services.Grounds.models import GroundUpdate
from Services.Grounds.update_ground import update_ground, update_facilities, update_equipments, update_pitches, \
    update_ground_images

router = APIRouter(
    prefix="/update_ground",
    tags=["Ground Update"],
)


@router.put("/ground/{id}")
async def ground_update(id: int, ground: dict, db: AsyncSession = Depends(get_db)):
    try:
        ground = GroundUpdate(**ground)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    await update_ground(ground_id=id, ground_data=ground, db=db)


@router.put("/facilities/{id}")
async def ground_facilities_update(id: int, facilities: dict, db: AsyncSession = Depends(get_db)):
    facility_list = facilities["facilities"]
    await update_facilities(ground_id=id, facilities_data=facility_list, db=db)


@router.put("/equipment/{id}")
async def ground_equipments_update(id: int, equipments: dict, db: AsyncSession = Depends(get_db)):
    equipment_list = equipments['equipment']
    await update_equipments(ground_id=id, equipments_data=equipment_list, db=db)


class Pitch(BaseModel):
    name: str
    description: str
    length: str
    width: str
    game_type: str
    price_per_60mins: str
    price_per_90mins: str

class PitchResponse(BaseModel):
    pitches: List[Pitch]

@router.put("/pitches/{ground_id}")
async def pitches_update(
    ground_id: int,
    pitches_data: PitchResponse,
    db: AsyncSession = Depends(get_db)
):
    try:
        logger = logging.getLogger(__name__)
        logger.error(pitches_data)
        pitches = pitches_data.pitches
        logger.error(pitches)
        logger.error('sabdhjsb')
        # for pitch in pitches:
        #     x = pitch.model_dump()
        #     logger.error(x)
        list_pitches = []
        for pitch in pitches:
            list_pitches.append(pitch.model_dump())
        logger.error(list_pitches)
        await update_pitches(ground_id=ground_id, pitches_data=list_pitches, db=db)
        return {"message": "Pitches updated successfully"}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)

class ImageUpdateRequest(BaseModel):
    images: List[str]  # Ensures only a list of strings is accepted


@router.put("/images/{ground_id}")
async def images_update(ground_id: int, images_data: ImageUpdateRequest, db: AsyncSession = Depends(get_db)):
    image_list = images_data.images  # Access images directly
    await update_ground_images(ground_id=ground_id, images_data=image_list, db=db)
    return {"message": "Images updated successfully"}
