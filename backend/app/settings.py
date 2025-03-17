from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, models, schemas

router = APIRouter()

@router.post("/change-password/", response_model=schemas.User)
def change_password(password_data: schemas.PasswordChange, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=password_data.username)
    if not user or not user.hashed_password == password_data.old_password + "notreallyhashed":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user.hashed_password = password_data.new_password + "notreallyhashed"
    db.commit()
    db.refresh(user)
    return user