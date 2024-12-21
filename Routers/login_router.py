from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from Database.Async_DB_Connection import get_db
from Services.Auth.Login.login import admin_login, LoginRequest

router = APIRouter(
    prefix="/login",
    tags=["Login Router"],
)

@router.post("/admin")
async def login_admin(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await admin_login(login_data, db=db)