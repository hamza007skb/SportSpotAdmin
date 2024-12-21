import base64
from PIL import Image
import io
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_owners_table, get_owner_image_table


async def get_all_owners(db: AsyncSession):
    try:
        # Define table references
        owners_table = await get_owners_table()          # Owners table
        owner_image_table = await get_owner_image_table()  # OwnerImage table

        # Query to get all owners along with their image
        query = (
            select(
                owners_table.c.email.label("owner_email"),
                owners_table.c.name.label("owner_name"),
                owners_table.c.phone_no.label("owner_phone"),
                owner_image_table.c.image_data.label("owner_image")
            )
            .outerjoin(
                owner_image_table, owners_table.c.email == owner_image_table.c.owner_email
            )
        )

        # Execute query
        result = await db.execute(query)
        owners = result.all()

        # Function to compress image
        def compress_image(image_data, quality=50, size=(100, 100)):
            try:
                img = Image.open(io.BytesIO(image_data))
                img = img.convert("RGB")  # Ensure format compatibility
                img.thumbnail(size)  # Resize image while maintaining aspect ratio
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=quality)
                return buffer.getvalue()
            except Exception as e:
                print(f"Image compression error: {e}")
                return image_data  # Return original if compression fails

        # Prepare response
        owner_list = []
        for owner in owners:
            compressed_image = None
            if owner.owner_image:
                # Compress the image data before encoding
                compressed_image_data = compress_image(owner.owner_image)
                compressed_image = base64.b64encode(compressed_image_data).decode('utf-8')

            owner_list.append({
                "email": owner.owner_email,
                "username": owner.owner_name,
                "phone": owner.owner_phone,
                "photo": compressed_image
            })

        return owner_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching owners: {e}")
