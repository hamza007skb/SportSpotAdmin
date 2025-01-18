from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_users_table, get_bookings_table, get_user_reviews_table


async def delete_user(email: str, db: AsyncSession):
    # Get tables
    users = await get_users_table()
    bookings = await get_bookings_table()
    reviews = await get_user_reviews_table()

    try:
        # Check if user exists
        query = select(users).where(users.c.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete related records in other tables
        delete_bookings_query = delete(bookings).where(bookings.c.user_email == email)
        delete_reviews_query = delete(reviews).where(reviews.c.user_id == email)
        await db.execute(delete_bookings_query)
        await db.execute(delete_reviews_query)

        # Delete the user
        delete_user_query = delete(users).where(users.c.email == email)
        await db.execute(delete_user_query)
        await db.commit()

        return {"message": f"User with email {email} and all related records deleted successfully"}

    except HTTPException as e:
        # Re-raise HTTPException errors for proper client response
        raise e

    except Exception as e:
        # Rollback transaction in case of failure
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")