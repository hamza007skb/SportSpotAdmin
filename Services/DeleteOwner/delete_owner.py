from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_owners_table



async def delete_owner(email: str, db: AsyncSession):
    try:
        Owners = await get_owners_table()
        # Query to check if the owner exists
        query = select(Owners).where(Owners.c.email == email)
        result = await db.execute(query)
        owner = result.fetchone()

        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found.")

        # Delete the owner
        delete_query = delete(Owners).where(Owners.c.email == email)
        await db.execute(delete_query)
        await db.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")