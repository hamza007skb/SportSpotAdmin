import logging

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_grounds_table, get_owners_table, get_users_table, get_bookings_table


async def get_user_bookings(user_email: str, session: AsyncSession):
    grounds_table = await get_grounds_table()
    owners_table = await get_owners_table()
    users_table = await get_users_table()
    bookings_table = await get_bookings_table()

    query = (
        select(
            owners_table.c.name.label("owner_name"),
            owners_table.c.phone_no.label("owner_no"),
            users_table.c.username.label("username"),
            users_table.c.email.label("email"),
            bookings_table.c.start_time,
            bookings_table.c.booking_date,
            grounds_table.c.name.label("ground_name"),
            grounds_table.c.address,
            bookings_table.c.payment_status
        )
        .join(grounds_table, bookings_table.c.ground_id == grounds_table.c.id)
        .join(owners_table, grounds_table.c.email == owners_table.c.email)
        .join(users_table, users_table.c.email == bookings_table.c.user_email)
        .where(bookings_table.c.user_email == user_email)
    )

    result = await session.execute(query)
    rows = result.fetchall()

    bookings = [
        {
            "owner_name": row.owner_name,
            "owner_phone": row.owner_no,
            "username": row.username,
            "email": row.email,
            "start_time": row.start_time,
            "booking_date": row.booking_date,
            "ground_name": row.ground_name,
            "address": row.address,
            "payment_status": row.payment_status,
        }
        for row in rows
    ]

    logging.error(f"bookings: {bookings}")

    return bookings


async def get_ground_bookings(session: AsyncSession, ground_id: int):

    grounds_table = await get_grounds_table()
    owners_table = await get_owners_table()
    users_table = await get_users_table()
    bookings_table = await get_bookings_table()

    query = (
        select(
            owners_table.c.name.label("owner_name"),
            owners_table.c.phone_no.label("owner_no"),
            users_table.c.username.label("username"),
            users_table.c.email.label("email"),
            bookings_table.c.start_time,
            bookings_table.c.booking_date,
            bookings_table.c.payment_status
        )
        .join(grounds_table, bookings_table.c.ground_id == grounds_table.c.id)
        .join(owners_table, grounds_table.c.email == owners_table.c.email)
        .join(users_table, users_table.c.email == bookings_table.c.user_email)
        .where(bookings_table.c.ground_id == ground_id)
    )

    result = await session.execute(query)
    rows = result.fetchall()

    # Transform results into a list of dictionaries
    bookings = [
        {
            "owner_name": row.owner_name,
            "owner_no": row.owner_no,
            "username": row.username,
            "email": row.email,
            "start_time": row.start_time.strftime("%H:%M:%S"),
            "booking_date": row.booking_date,
            "payment_status": row.payment_status,
        }
        for row in rows
    ]