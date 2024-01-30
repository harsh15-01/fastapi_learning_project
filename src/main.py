from fastapi import FastAPI
from src.assignments.assignment01.assignment01 import user_router, brand_router, brandAdd_router, brandUpdate_router, brandDelete_router

app = FastAPI()

# Include API routes
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(brand_router, prefix="/story", tags=["story"])
app.include_router(brandAdd_router, prefix="/brand_create", tags=["brand"])
app.include_router(brandUpdate_router, prefix="/brand_settings", tags=[""])
app.include_router(brandDelete_router,prefix="/brand_delete", tags=[""])


def get_app():
    return app
