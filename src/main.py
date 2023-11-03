from fastapi import FastAPI

from views.health import router as health_router


app = FastAPI(
    title="Cross Post APi",
    description="API to cross-post a postcards among users",
)


app.include_router(health_router)
