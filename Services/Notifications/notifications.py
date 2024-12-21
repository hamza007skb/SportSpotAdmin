from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from Database.async_tables import get_admin_notifications_table


from sqlalchemy import update, select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

async def read_notification(notification_id: int, db: AsyncSession):
    try:
        # Reflect the table
        admin_notifications_table = await get_admin_notifications_table()

        # Query the notification by ID
        query = select(admin_notifications_table).where(admin_notifications_table.c.id == notification_id)
        result = await db.execute(query)
        notification = result.fetchone()

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        # Update the notification's read status to True if not already read
        if not notification.read:
            stmt = (
                update(admin_notifications_table)
                .where(admin_notifications_table.c.id == notification_id)
                .values(read=True)
            )
            await db.execute(stmt)
            await db.commit()

            # Fetch the updated notification details
            result = await db.execute(query)
            notification = result.fetchone()

        # Convert the notification row into a dictionary
        notification_dict = dict(notification._mapping)  # Accessing _mapping to convert the Row to a dictionary

        # Return the updated notification details
        return {
            "id": notification_dict["id"],
            "subject": notification_dict["subject"],
            "body": notification_dict["body"],
            "created_at": notification_dict["created_at"],
            "read": notification_dict["read"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_single_notification(notification_id: int, db: AsyncSession):
    try:
        admin_notifications_table = await get_admin_notifications_table()
        query = select(admin_notifications_table).where(admin_notifications_table.c.id == notification_id)
        notification = await db.execute(query)

        notification = notification.fetchone()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        return {
            "id": notification.id,
            "subject": notification.subject,
            "body": notification.body,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_notifications(db: AsyncSession):
    try:
        # Reflect the table
        admin_notifications_table = await get_admin_notifications_table()

        # Query to fetch all notifications
        query = select(admin_notifications_table)
        result = await db.execute(query)
        notifications = result.fetchall()

        # Convert notifications to a list of dictionaries
        notifications_list = [
            {
                "id": notification.id,
                "subject": notification.subject,
                "body": notification.body,
                "created_at": notification.created_at,
                "read": notification.read,
            }
            for notification in notifications
        ]

        return {"notifications": notifications_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def mark_all_notifications_as_read(db: AsyncSession):
    try:
        # Reflect the table
        admin_notifications_table = await get_admin_notifications_table()

        # Update all notifications to mark them as read
        stmt = update(admin_notifications_table).values(read=True)
        await db.execute(stmt)
        await db.commit()

        return {"message": "All notifications marked as read"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
