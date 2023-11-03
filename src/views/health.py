from fastapi import APIRouter

from models.health import HealthCheckResponse
from database.main import Database


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/health")
async def health() -> HealthCheckResponse:
    """Checks availability of the API and the database."""
    db_status = Database.health_check()
    return HealthCheckResponse(api_status="ok", db=db_status)
