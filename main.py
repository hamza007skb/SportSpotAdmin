from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Routers import signup_router, stats_router, notifications_router, login_router, \
    users_info_router, owner_info_router, ground_list_router, ground_detail_router, add_ground_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(signup_router.router)
app.include_router(stats_router.router)
app.include_router(notifications_router.router)
app.include_router(login_router.router)
app.include_router(users_info_router.router)
app.include_router(owner_info_router.router)
app.include_router(ground_list_router.router)
app.include_router(ground_detail_router.router)
app.include_router(add_ground_router.router)

