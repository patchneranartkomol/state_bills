from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import crud, models, schemas
from .constants import STATES
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


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(exc)
    )


response_models = {'200': {'model': List[schemas.Bill]},
                   '400': {'model': schemas.HTTPError}}
@app.get("/bills/{state}", responses=response_models)
def read_state_bills(state: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    if state not in STATES:
        raise HTTPException(status_code=404, detail='Not a valid US state')
    bills = crud.get_state_bills(db, state, skip, limit)
    return bills
