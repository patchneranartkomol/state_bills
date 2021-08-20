from datetime import date
from typing import List, Optional

from pydantic import BaseModel


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
    state: str
    session: str
    session_id: int


class BillCreate(BillBase):
    change_hash: str
    url: str


class Bill(BillBase):

    class Config:
        orm_mode = True
