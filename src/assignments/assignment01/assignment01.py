from src.assignments.assignment01.utils import read_user, read_story_data, create_brand,update_brand, delete_brand
from src.database import get_db
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

user_router = APIRouter()


@user_router.get("/{user_id}")
def read_user_endpoint(user_id: int, brand_id: int, db: Session = Depends(get_db)):
    return read_user(user_id, brand_id, db)


brand_router = APIRouter()


@brand_router.get("/{user_id}")
def read_story_data_endpoint(owner_id: int, id: int, db: Session = Depends(get_db)):
    return read_story_data(owner_id, id, db)


brandAdd_router = APIRouter()


@brandAdd_router.post("/{user_id}")
def create_brand_endpoint(user_id: int, brand_data: dict, db: Session = Depends(get_db)):
    return create_brand(user_id, brand_data, db)


brandUpdate_router = APIRouter()


@brandUpdate_router.put("/user/{user_id}/brand/{brand_id}")
def update_brand_endpoint(user_id: int, brand_id: int,rec:dict, db: Session = Depends(get_db)):
    return update_brand(user_id, brand_id, rec,db)


brandDelete_router = APIRouter()


@brandDelete_router.delete("/user/{user_id}")
def delete_brand_endpoint(user_id: int, req:dict, db: Session = Depends(get_db)):
    return delete_brand(user_id,req,db)