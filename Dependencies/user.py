
from typing import Annotated
from ..database import models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..database.databaseConnition import get_db 


async def add_user(db: Annotated[Session, Depends(get_db)], inputs: schemas.UserCreate):
    try :
        user = db.query(models.Users).filter(models.Users.email == inputs.email).first()
        if user:
            print('user already exists')
            raise HTTPException(status_code=400, detail="User already exists")
        user = models.Users(**inputs.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except :
        raise HTTPException(status_code=400, detail="Something went wrong")



async def get_user(id_usesr: int, db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Users).filter(models.Users.id == id_usesr).first()
