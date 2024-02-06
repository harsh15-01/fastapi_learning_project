import json
from typing import Dict, Union, Any
from fastapi import Depends, HTTPException, APIRouter, Cookie
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import BrandSettings, Story, Brand, Account, User
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


class CreateUserRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    primary_coach_mail: str
    secondary_coach_mail: int
    account_id: int


class UpdateBrandSettings(BaseModel):
    name: str
    url: str
    bucket: str


def process_user_data(user_create: CreateUserRequest):
    processed_user_data = {
        "username": user_create.firstname + " " + user_create.lastname,
        "firstName": user_create.firstname,
        "lastName": user_create.lastname,
        "email": user_create.email,
        "secondary_email": user_create.primary_coach_mail,
        "account_id": user_create.account_id
    }
    return processed_user_data


def update_user_data(user_data: UpdateBrandSettings):
    updated_user_data = {
        "name": user_data.name,
        "url": user_data.url,
        "bucket": user_data.bucket
    }


def response(Data):
    return {
        "success": True,
        "statusCode": 200,
        "data": Data
    }


@router.post("/user_id")
def create_user(data: dict = Depends(process_user_data), db: Session = Depends(get_db)):
    try:
        user = User()
        user.username = data["username"]
        user.firstname = data["firstName"]
        user.lastname = data["lastName"]
        user.email = data["email"]
        user.secondary_email = data["secondary_email"]
        user.account_id = data["account_id"]
        db.add(user)
        db.commit()
        db.refresh(user)
        query = db.query(User.id.label("user_id"), Account.id.label("account_id"), Brand.name.label("brand_name"),
                         Brand.id.label("brand_id")).filter(Account.id == user.account_id, user.id == user.id) \
            .join(Brand, Brand.id == Account.brandName).first()
        query_dict = {
            "user_id": query.user_id,
            "brand_id": query.brand_id,
            "brand_name": query.brand_name,
            "account_id": query.account_id,
        }
        # print("<<<<<<<<<<<<")
        # print(query_dict.user_id, query_dict.brand_id, query_dict.brand_name)
        return JSONResponse(status_code=200, content={"message": "User created successfully", "data": query_dict})
    except Exception as e:
        return JSONResponse(status_code=400, content={"something went wrong!"})


@router.post('/get_story')
def get_story(user_id: int = Cookie(), db: Session = Depends(get_db)):
    try:
        query_results = db.query(User.id.label("user_id"), Account.id.label("account_id"), Brand.id.label("brand_id"),
                                 Story.id, Story.title) \
            .filter(User.id == user_id, Story.inactive == 0) \
            .join(Brand, Story.brand_id == Brand.id) \
            .join(Account, Brand.id == Account.brandName) \
            .join(User, Account.id == User.account_id).all()

        result = {"user_id": None, "account_id": None, "brand_id": None, "stories": []}

        for row in query_results:
            if result["user_id"] is None:
                result["user_id"] = row.user_id
                result["account_id"] = row.account_id
                result["brand_id"] = row.brand_id

            result["stories"].append({"story_id": row.id, "story_title": row.title})
        return response(result)
    except:
        return JSONResponse(status_code=400, content={"message": "something went wrong!"})


@router.put('/update_status')
def update_status(user_ids: str = Cookie(), statuses: str = Cookie(), db: Session = Depends(get_db)):
    try:
        user_ids_list = [int(user_id) for user_id in user_ids.split(" ")]
        status_list = [int(status) for status in statuses.split(" ")]

        for user_id, inactive in zip(user_ids_list, status_list):
            db.query(User).filter(User.id == user_id).update({"inactive": inactive})
        db.commit()

        response_data = [
            {"user_id": user_id, "status": status} for user_id, status in zip(user_ids_list, status_list)
        ]
        return response(response_data)
    except:
        return JSONResponse(status_code=400, content={"message": "something went wrong!"})


@router.post('/loggedIn_id')
def new_entry(data: dict = Depends(update_user_data), loggedIn_id: int = Cookie(), db: Session = Depends(get_db)):
    print(loggedIn_id)
    print("<<<<<<<<<<<<<<")
    try:
        query = db.query(User, BrandSettings).filter(User.id == loggedIn_id, BrandSettings.inactive_settings == 0) \
            .join(Account, User.account_id == Account.id) \
            .join(Brand, Account.brandName == Brand.id) \
            .join(BrandSettings, Brand.id == BrandSettings.brand_id).first()

        print(query.User.id,"<<<<<<<<<<<<<<",query.BrandSettings.inactive_settings)

        db.query(BrandSettings).filter(BrandSettings.id == query.BrandSettings.brand_id) \
            .update({"inactive_settings": 1})
        db.commit()

        # Fetch the updated record
        updated_brand_settings = db.query(BrandSettings).filter(BrandSettings.id == query.BrandSettings.brand_id).first()

        # Print the updated value
        print("Updated inactive_settings:", updated_brand_settings.inactive_settings)

        # new_brandSetting_data = get_modified_data(query_results.BrandSettings, bsModel)
        # new_data = BrandSettings(**new_brandSetting_data)
        # db.add(new_data)
        # db.commit()
        # db.refresh(new_data)
        # new = BrandSettings()
        # new.name = data["name"]
        # new.url = data["url"]
        # new.bucket = data["bucket"]
        # db.add(new)
        # db.commit()
        # db.refresh(new)
        # print("<<<<<<<<<<<", new.name, new.url, new.bucket)
    except:
        return JSONResponse(status_code=400, content={"message": "something went wrong!"})
