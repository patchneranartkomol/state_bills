from sqlalchemy.orm import Session

from . import models, schemas


def get_bills(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Bill).offset(skip).limit(limit).all()
