from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/bills/", response_model=List[schemas.Bill])
def read_items(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    bills = crud.get_bills(db, skip=skip, limit=limit)
    return bills
