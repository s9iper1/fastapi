import os
from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from config.db import SessionLocal
from models.user import Users
from schemas.index import User

user = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user.get("/get_all_users/")
async def get_all_user(db: Session = Depends(get_db)):
    # return db.execute(Users.select()).fetchall()
    print(db.query(Users).all())
    return db.query(Users).all()


@user.get("/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(Users).filter(Users.id == id).first()


@user.post("/")
async def add_user(user: User, db: Session = Depends(get_db)):
    db_user = Users(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user.patch("/{id}")
async def update_user(id: int, user: User, db: Session = Depends(get_db)):
    stored_item_data = db.query(Users).filter(Users.id == id).first()
    if not stored_item_data:
        raise HTTPException(status_code=404, detail="User not found")
    hero_data = user.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(stored_item_data, key, value)
    db.add(stored_item_data)
    db.commit()
    db.refresh(stored_item_data)
    return stored_item_data


@user.put("/{id}")
async def update_user(id: int, user: User, db: Session = Depends(get_db)):
    stored_item_data = db.query(Users).filter(Users.id == id).first()
    if not stored_item_data:
        raise HTTPException(status_code=404, detail="User not found")
    hero_data = user.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(stored_item_data, key, value)
    db.add(stored_item_data)
    db.commit()
    db.refresh(stored_item_data)
    return stored_item_data


@user.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()


@user.post("/profile_picture/{id}")
async def profile_picture(id: int, file: UploadFile | None = File(default=None), db: Session = Depends(get_db)):
    current_path = Path().absolute()
    folder = os.path.join(current_path, 'media')
    check_folder = os.path.exists(folder)
    if not check_folder:
        print("Media folder NOT exists")
        os.makedirs(os.path.join(folder))
    print("Directory Path:", Path().absolute())  # Directory of current working directory, not __file__
    # start saving file
    complete_name = os.path.join(folder, file.filename)
    try:
        contents = file.file.read()
        with open(complete_name, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    stored_item_data = db.query(Users).filter(Users.id == id).first()
    if not stored_item_data:
        raise HTTPException(status_code=404, detail="User not found")
    stored_item_data.profile_image = file.filename
    db.add(stored_item_data)
    db.commit()
    db.refresh(stored_item_data)
    return stored_item_data


@user.get("/my_profile_picture/{id}")
async def get_profile_picture(id: int, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    profile_pic = db_user.profile_image
    return profile_pic
