from calendar import month
import imp
from pydantic import BaseModel

class Month(BaseModel):
    
    month : str
    year : str
    class Config:
        orm_mode = True
class out_Month(Month):    
    id : int
    user_id : str
    class Config:
        orm_mode = True
class out2_Month(out_Month):    
    amount : int = 0
    class Config:
        orm_mode = True
        validate_assignment = True