from sqlalchemy import Column, ForeignKey, Integer, String
from ..db_setup import Base

class Month(Base):
    __tablename__ = "Month"
    id = Column(Integer, primary_key=True, index=True,nullable=False)
    month = Column(String(10), nullable=False)
    year = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    