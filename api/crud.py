from sqlalchemy.orm import Session

from . import models, schemas


def get_state_bills(db: Session, state: str, skip: int = 0, limit: int = 50):
    return db.query(models.Bill).filter_by(state=state).offset(skip).limit(limit).all()
