import json
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import BrandSettings, Story, Brand


def read_user(user_id: int, brand_id: int, db: Session = Depends(get_db)):
    user_obj = db.query(BrandSettings.settings_json).filter(BrandSettings.inactive_settings == 0,
                                                            BrandSettings.brand_id == brand_id,
                                                            BrandSettings.id == user_id).all()
    title = user_obj[0][0] if user_obj else ""
    return {"success": True, "user_id": user_id, "brand_id": brand_id, "setting_json": title}


def read_story_data(owner_id: int, id: int, db: Session = Depends(get_db)):
    user_obj = db.query(Story.title).filter(Story.id == id).all()
    title = user_obj[0] if user_obj else ""
    return {"success": True, "story_title": title, "owner_id": owner_id}


def create_brand(user_id: int, brand_data: dict, db: Session = Depends(get_db)):
    brand_data["created_by"] = user_id
    brand_data["updated_by"] = user_id
    new_brand = Brand(**brand_data)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return {"success": True}


def update_brand(id:int, brand_id:int, rec:dict, db: Session = Depends(get_db)):
    user_obj = db.query(BrandSettings).filter(BrandSettings.id == id, BrandSettings.brand_id==brand_id).first()
    if user_obj:
        existing_data = json.loads(user_obj.settings_json)
        existing_data.update(rec)
        user_obj.settings_json = json.dumps(existing_data)
        db.commit()
        return {"success": True}


def delete_brand(user_id:int,req:dict,db: Session = Depends(get_db)):
    db.query(Story).filter(Story.owner_id == user_id, Story.id==req["story_id"]).delete()
    db.commit()
    return {"success": True}