import json
from typing import Dict, Union, Any
from fastapi import Depends, HTTPException, APIRouter, Cookie, Request, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import BrandSettings, Story, Brand, Account, User, BrandTelephonySetting, Language
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.assignments.assignment03.utils import getResposne, validate_user_id, validate_account_id, validate_admin_user_id
from src.assignments.assignment03.schema import UserUpdate

router3 = APIRouter()


@router3.get("/user_id")
def get_user_data(request: Request, db: Session = Depends(get_db)):
    """accepts user_id and account_id from cookies and checks the brand settings
    for that user and returns the multilingual_support and preferred_language field
    a JSON response"""
    try:
        user_id = validate_user_id(request,db)
        account_id = validate_account_id(request,db)
        result = db.query(BrandSettings, User, Account).filter(User.id == user_id, User.account_id == account_id) \
            .join(Account, User.account_id == Account.id) \
            .join(Brand, Account.brandName == Brand.id) \
            .join(BrandSettings, BrandSettings.brand_id == Brand.id).first()
        if result is not None:
            b_id = result.BrandSettings.brand_id
            settings_json = json.loads(result.BrandSettings.settings_json)
            if settings_json is not None:
                multilingual_support = settings_json.get("multilingual_support")
                preferred_language = settings_json.get("preferred_language")
            else:
                return getResposne(data="Settings JSON not found for the specified user and account",status_code=status.HTTP_404_NOT_FOUND)
            query = db.query(Language).filter(Language.code == preferred_language).first()
            return JSONResponse(content={"status_code":status.HTTP_200_OK,"Brand ID": b_id, "Multilingual Support:": multilingual_support,
                                         "Preferred Language:": query.name})
        else:
            return getResposne(data="BrandSettings not found for the specified user and account",status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"data": f"Something went wrong. {e}"})


@router3.get("/id")
def get_ivr_number(request: Request, db: Session = Depends(get_db)):
    """accepts user_id from the cookies and checks the brand_id fo that user and
    returns the ivr_number of the user and returns an error message if no telephony
    is available for that user"""
    try:
        user_id = validate_user_id(request,db)
        result = db.query(BrandTelephonySetting, Brand, User, Account).filter(User.id == user_id,\
                                                                              BrandTelephonySetting.brand_id == Brand.id) \
            .join(Brand, Brand.id == BrandTelephonySetting.brand_id) \
            .join(Account, Account.brandName == Brand.id) \
            .join(User, User.account_id == Account.id).all()
        if not result:
            return getResposne(data="Telephony settings not found for the specified brand_id",status_code=status.HTTP_404_NOT_FOUND)

        ivr_numbers = [result[0].ivr_number for result in result]
        return JSONResponse(content={"status_code": status.HTTP_200_OK, "message":"User fetched successfully", "IVR Number": ivr_numbers})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"data": f"Something went wrong.{e}"})


@router3.put("/admin_user_id")
async def update_record(user_update: UserUpdate, request: Request, db: Session = Depends(get_db)):
    """accepts user_id from request body and admin_user_id from cookies and
     updates the fields provided by the user in the request body if both user_id
      and admin_user_id belong to same brand"""
    try:
        user_id = validate_user_id(request,db)
        admin_user_id = validate_admin_user_id(request,db)
        user = db.query(User).filter(User.id == user_id).first()
        admin_user = db.query(User).filter(User.id == admin_user_id).first()
        if user is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"data": f"User with id {user_id} not found."})
        if admin_user is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"data": f"Admin user with id {admin_user_id} not found."})
        for field, value in user_update.dict().items():
            if field != "id":
                setattr(user_update, field, value)
        db.commit()
        return JSONResponse(content={"status_code":status.HTTP_200_OK, "data": "User updated successfully"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": f"Something went wrong. {e}"})
