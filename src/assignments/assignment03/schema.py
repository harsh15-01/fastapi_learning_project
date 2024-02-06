from pydantic import BaseModel
from typing import Optional
from src.model import User
from datetime import datetime
import json


class UserUpdate(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    title: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    secondary_email: Optional[str] = None
    defaultEmail: Optional[int] = None
    password: Optional[str] = None
    image: Optional[bytes] = None
    account_id: Optional[int] = None
    last_login_time: Optional[datetime] = None
    created_time: Optional[datetime] = None
    inactive: Optional[int] = None
    inactive_datetime: Optional[datetime] = None
    signature: Optional[str] = None
    coach_id: Optional[int] = None
    secondary_coach_id: Optional[int] = None
    timezone_offset: Optional[float] = None
    timezone: Optional[int] = None
    brand_id: Optional[int] = None
    terms_accepted_datetime: Optional[datetime] = None
    passwordchanged_time: Optional[datetime] = None
    otp: Optional[str] = None
    thumbnail: Optional[str] = None
    jwt_access_token: Optional[str] = None
    jwt_refresh_token: Optional[str] = None
    previous_password: Optional[str] = None
