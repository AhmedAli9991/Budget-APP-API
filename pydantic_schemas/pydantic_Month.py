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
