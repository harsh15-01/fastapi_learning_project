from fastapi.responses import JSONResponse
from fastapi import Request, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import User


def getResposne(data=None, status_code=None):
    """response body for api request"""
    status_code = 200 if status_code is None else status_code
    returning_data = data if data is not None else {}
    data = {
        "status": status_code,
        "data": returning_data
    }
    return JSONResponse(status_code=status_code, content=data)


def validate_user_id(request: Request, db: Session = Depends(get_db)) -> int:
    """Validate and retrieve user_id from cookies."""
    user_id = request.cookies.get("user_id", None)
    if user_id is None or not user_id.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Provide user_id as a positive integer in the cookie")
    user_id = int(user_id)
    if user_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id should be a positive integer")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found, Please try again")
    return user_id


def validate_account_id(request: Request, db: Session = Depends(get_db)) -> int:
    """Validate and retrieve account_id from cookies."""
    account_id = request.cookies.get("account_id", None)
    if account_id is None or not account_id.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Provide account_id as a positive integer in the cookie")
    account_id = int(account_id)
    if account_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="account_id should be a positive integer")
    user = db.query(User).filter(User.account_id == account_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found for the specified account_id")
    return account_id


def validate_admin_user_id(request: Request, db: Session = Depends(get_db)):
    """validate and retrieve admin_user_id from cookies."""
    admin_user_id = request.cookies.get("admin_user_id", 0)
    if admin_user_id is None or not admin_user_id.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Provide admin_id as a positive integer in the cookie")
    admin_user_id = int(admin_user_id)
    admin_user = db.query(User).filter(User.id == admin_user_id).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found for the specified admin_id")
    return admin_user_id