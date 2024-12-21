from sqlalchemy import select, func
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_users_table, get_bookings_table

async def get_all_users(db: AsyncSession):
    try:
        # Get the Users and Bookings table
        user_table = await get_users_table()  # Users table
        bookings_table = await get_bookings_table()  # Bookings table

        # Query to join Users and Bookings to count total bookings
        query = (
            select(
                user_table.c.email,
                user_table.c.username,
                func.count(bookings_table.c.id).label("total_bookings")
            )
            .outerjoin(
                bookings_table, user_table.c.email == bookings_table.c.user_email
            )
            .group_by(user_table.c.email, user_table.c.username)
        )

        # Execute the query
        result = await db.execute(query)
        users = result.all()

        # Return structured response
        return [
            {
                "email": user.email,
                "username": user.username,
                "bookings": user.total_bookings
            }
            for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")