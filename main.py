from fastapi import FastAPI
from Routers import signup_router


app = FastAPI()
app.include_router(signup_router.router)
