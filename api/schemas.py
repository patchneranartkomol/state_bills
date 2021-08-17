from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class BillBase(BaseModel):
    bill_id: int
    # Legislative bill numbers are strings - i.e. 'AB6'
    number: str
    change_hash: str
    url: str
    status_date: date
    status: int
    last_action_date: date
    last_action: str
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BillCreate(BillBase):
    pass
