from pydantic import BaseModel

class Monthly_transaction(BaseModel):
    name : str
    amount : int
class out_transaction(Monthly_transaction):
    id : int
    month_id :int
    class Config:
        orm_mode = True
        