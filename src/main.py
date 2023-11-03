from fastapi import FastAPI

from views.health import router as health_router
from views.authorization import router as auth_router
from views.users import router as users_router


app = FastAPI(
    title="Cross Post APi",
    description="API to cross-post a postcards among users",
)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
