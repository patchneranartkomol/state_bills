from sqlalchemy import Column, Date, Integer, String

from .database import Base


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, index=True)
    # Legislative bill numbers are strings - i.e. 'AB6'
    number = Column(String)
    change_hash = Column(String)
    url = Column(String)
    status_date = Column(Date)
    status = Column(Integer)
    last_action_date = Column(Date)
    last_action = Column(String)
    title = Column(String)
    description = Column(String)
