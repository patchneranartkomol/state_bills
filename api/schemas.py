from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .constants import STATES


StateEnum = Enum('StateEnum', {st: st for st in STATES})


class BillBase(BaseModel):
    bill_id: int
    # Legislative bill numbers are strings - i.e. 'AB6'
    number: str
    status_date: Optional[date] = None
    status: int
    last_action_date: Optional[date] = None
    last_action: str
    title: str
    description: Optional[str] = None
    state: StateEnum
    session: str
    session_id: int


class BillCreate(BillBase):
    change_hash: str
    url: str


class Bill(BillBase):

    class Config:
        orm_mode = True


class HTTPError(BaseModel):
    """
    HTTP error schema to be used when an `HTTPException` is thrown.
    """
    detail: str
