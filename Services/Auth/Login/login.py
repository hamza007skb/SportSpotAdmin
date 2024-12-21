from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from Database.async_tables import get_admins_table

class LoginRequest(BaseModel):
    email: str
    password: str



async def admin_login(login_data: LoginRequest, db: AsyncSession):
    # Get the Admins table
    Admins = await get_admins_table()

    # Query the database for an admin with the provided email and password
    query = (
        select(Admins)
        .where(and_(
            Admins.c.email == login_data.email,
            Admins.c.hashed_password == login_data.password
        ))
    )
    result = await db.execute(query)
    admin = result.fetchone()

    # If no admin found, raise a 401 error
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Return a success response with the admin's email
    return {"message": "Login successful!", "email": login_data.email}