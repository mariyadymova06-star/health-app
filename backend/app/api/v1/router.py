from fastapi import APIRouter
from app.api.v1 import auth, profile, measurements, goals, dashboard

router = APIRouter(prefix="/api/v1")
router.include_router(auth.router)
router.include_router(profile.router)
router.include_router(measurements.router)
router.include_router(goals.router)
router.include_router(dashboard.router)
