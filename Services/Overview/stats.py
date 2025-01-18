import logging

from sqlalchemy import select, func, case, and_, extract, text, Float, cast, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_users_table, get_grounds_table, get_bookings_table, get_pitches_table

async def get_user_count(db: AsyncSession):
    users_table = await get_users_table()
    query = select(func.count(users_table.c.email))
    db_result = await db.execute(query)
    count = db_result.scalar()

    return count

async def get_ground_count(db: AsyncSession):
    ground_table = await get_grounds_table()
    query = select(func.count(ground_table.c.id))
    db_result = await db.execute(query)
    count = db_result.scalar()

    return count

async def get_booking_count(db: AsyncSession):
    bookings_table = await get_bookings_table()
    query = select(func.count(bookings_table.c.id))
    db_result = await db.execute(query)
    count = db_result.scalar()

    return count


async def get_total_revenue(db: AsyncSession):
    query = text("""
        SELECT 
            SUM(
                CASE 
                    WHEN B.duration = '60 minutes' THEN CAST(P.price_per_60mins AS NUMERIC)
                    WHEN B.duration = '90 minutes' THEN CAST(P.price_per_90mins AS NUMERIC)
                END
            ) AS total_revenue
        FROM 
            Bookings B
        JOIN 
            Pitches P ON B.ground_id = P.ground_id AND B.pitch_name = P.name
        WHERE 
            B.payment_status = 'paid';
        """)

    # Execute the query
    db_result = await db.execute(query)
    total_revenue = db_result.scalar()
    return total_revenue


async def get_stats(db: AsyncSession):
    users = await get_user_count(db)
    ground_s = await get_ground_count(db)
    bookings = await get_booking_count(db)
    total_revenue = await get_total_revenue(db)
    logging.info(f'revenue: {total_revenue}')

    # Reflect tables
    users_table = await get_users_table()
    grounds_table = await get_grounds_table()
    bookings_table = await get_bookings_table()
    pitches_table = await get_pitches_table()

    # Query for total stats
    stats_query = select(
        func.sum(
            case(
                (and_(
                    bookings_table.c.payment_status == 'paid',
                    bookings_table.c.duration == text("'60 minutes'::INTERVAL")
                ), pitches_table.c.price_per_60mins.cast(Float)),
                (and_(
                    bookings_table.c.payment_status == 'paid',
                    bookings_table.c.duration == text("'90 minutes'::INTERVAL")
                ), pitches_table.c.price_per_90mins.cast(Float)),
                else_=0.0  # Match Float data type
            )
        ).label("last_month_revenue")
    ).select_from(
        users_table
        .join(bookings_table, bookings_table.c.user_email == users_table.c.email)
        .join(grounds_table, bookings_table.c.ground_id == grounds_table.c.id)
        .join(
            pitches_table,
            and_(
                bookings_table.c.ground_id == pitches_table.c.ground_id,
                bookings_table.c.pitch_name == pitches_table.c.name
            )
        )
    ).where(
        extract('month', bookings_table.c.booking_date) == extract('month', func.now()) - 1
    )

    result = await db.execute(stats_query)
    stats = result.fetchone()


    return {
        "total_users": users or 0,
        "total_grounds": ground_s or 0,
        "total_bookings": bookings or 0,
        "last_month_revenue": float(stats.last_month_revenue or 0),
        "total_revenue": float(total_revenue or 0),
    }