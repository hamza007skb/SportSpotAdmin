import base64
from typing import List

from PIL import Image
import io
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from Database.async_tables import get_grounds_table, get_ground_images_table, get_ground_owners_table
from Services.Grounds.models import GroundResponseModel


async def get_grounds_by_owner(owner: str, db: AsyncSession):
    try:
        grounds_table = await get_grounds_table()
        ground_owners_table = await get_ground_owners_table()

        query = (
            select(
                grounds_table.c.id.label("id"),
                grounds_table.c.name.label("name"),
                grounds_table.c.city.label("city"),
                grounds_table.c.country.label("country"),
                grounds_table.c.address.label("address"),
                grounds_table.c.description.label("description"),
                grounds_table.c.rating.label("rating"),
                grounds_table.c.total_ratings.label("total_ratings"),
            )
            .join(ground_owners_table, grounds_table.c.id == ground_owners_table.c.ground_id)
            .where(ground_owners_table.c.owner_email == owner)
        )

        result = await db.execute(query)
        grounds = result.fetchall()

        return [
            {
                "id": ground.id,
                "name": ground.name,
                "city": ground.city,
                "country": ground.country,
                "address": ground.address,
                "description": ground.description,
                "rating": ground.rating,
                "total_ratings": ground.total_ratings,
            }
            for ground in grounds
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching grounds: {e}")


async def get_photos_by_ground(groundId: int, db: AsyncSession):
    try:
        ground_images_table = await get_ground_images_table()

        query = select(ground_images_table.c.image_data).where(
            ground_images_table.c.ground_id == groundId
        )

        result = await db.execute(query)
        images = result.fetchall()

        # Function to compress and encode images
        def compress_and_encode(image_data, quality=50, size=(150, 150)):
            try:
                img = Image.open(io.BytesIO(image_data))
                img = img.convert("RGB")
                img.thumbnail(size)
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=quality)
                return base64.b64encode(buffer.getvalue()).decode("utf-8")
            except Exception as e:
                print(f"Image compression error: {e}")
                return base64.b64encode(image_data).decode("utf-8")

        return [compress_and_encode(record.image_data) for record in images]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching photos: {e}")


async def get_all_grounds(db: AsyncSession) -> List[GroundResponseModel]:
    # Fetch the grounds table
    grounds_table = await get_grounds_table()
    query = select(grounds_table)
    result = await db.execute(query)
    rows = result.mappings().all()
    grounds = [GroundResponseModel(**row) for row in rows]

    return grounds


async def get_ground_images(id: int, db: AsyncSession):
    ground_img = await get_ground_images_table()
    query = select(ground_img.c.image_data).where(ground_img.c.ground_id == id)
    result = await db.stream(query)

    images_base64 = []

    async for row in result:
        image_data = row[0]  # `row` is a tuple, and image_data is the first element
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        images_base64.append(image_base64)

    if not images_base64:
        raise HTTPException(status_code=404, detail="No images found for the specified ground ID")
    return JSONResponse(content={"images": images_base64})