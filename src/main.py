from fastapi import FastAPI
from src.assignments.assignment01.assignment01 import user_router, brand_router, brandAdd_router, brandUpdate_router, brandDelete_router
from src.assignments.assignment02.assignment02 import router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(brand_router, prefix="/story", tags=["story"])
app.include_router(brandAdd_router, prefix="/brand_create", tags=["brand"])
app.include_router(brandUpdate_router, prefix="/brand_settings", tags=["brand"])
app.include_router(brandDelete_router,prefix="/brand_delete", tags=["brand"])
app.include_router(router)


def get_app():
    return app
