from sqlalchemy import select, func, case, and_, extract, text, Float
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_users_table, get_grounds_table, get_bookings_table, get_pitches_table


async def get_stats(db: AsyncSession):
    # Reflect tables
    users_table = await get_users_table()
    grounds_table = await get_grounds_table()
    bookings_table = await get_bookings_table()
    pitches_table = await get_pitches_table()

    # Query for total stats
    stats_query = select(
        func.count(users_table.c.email).label("total_users"),
        func.count(grounds_table.c.id).label("total_grounds"),
        func.count(bookings_table.c.id).label("total_bookings"),
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
        ).label("last_month_revenue"),
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
        ).label("total_revenue")
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
        "total_users": stats.total_users or 0,
        "total_grounds": stats.total_grounds or 0,
        "total_bookings": stats.total_bookings or 0,
        "last_month_revenue": float(stats.last_month_revenue or 0),
        "total_revenue": float(stats.total_revenue or 0),
    }