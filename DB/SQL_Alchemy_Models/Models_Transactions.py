from sqlalchemy import Column, ForeignKey, Integer, String, false
from ..db_setup import Base

class Transaction(Base):
    __tablename__ = "Transaction"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    amount= Column(Integer,nullable=False)
    month_id = Column(Integer,ForeignKey("Month.id" ,ondelete="CASCADE"),nullable=False)
    