from fastapi import APIRouter,Depends, status, HTTPException
from pydantic_schemas import pydantic_Month
from Utils.JWT import get_current_user
from DB.db_setup import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from DB.SQL_Alchemy_Models.Models_Month import Month 
from DB.SQL_Alchemy_Models.Models_Transactions import Transaction 

router = APIRouter()

@router.get('/getMonth',status_code=status.HTTP_200_OK)
def get_months(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
   # months = db.query(Month).filter(Month.user_id==current_user["id"]).all()
    months =db.query(Month,func.sum(Transaction.amount).label('amount')).join(Transaction,Month.id==Transaction.month_id,isouter=True).filter(Month.user_id==current_user["id"]).group_by(Month.id).all()
    return months

@router.post('/addMonth',status_code=status.HTTP_201_CREATED, response_model= pydantic_Month.out_Month)
def add_months(new_month:pydantic_Month.Month ,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    found= db.query(Month).filter(Month.month==new_month.month,Month.year==new_month.year).first()
    if found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already exists")
    data={**new_month.dict(),"user_id":current_user["id"]}
    new = Month(**data)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new
    
@router.delete('/delete/{id}',status_code=status.HTTP_200_OK, response_model= str)
def delete_month(id:int,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)   
    qmonth = db.query(Month).filter(Month.id==id)
    month=qmonth.first()
    if(month == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    qmonth.delete(synchronize_session=False)
    db.commit()
    return "deleted"

@router.put('/update/{id}',status_code=status.HTTP_200_OK, response_model= str)
def change_month(id:int,updated:pydantic_Month.Month,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)   
    qmonth = db.query(Month).filter(Month.id==id)
    month=qmonth.first()
    if(month == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    qmonth.update(updated.dict(), synchronize_session=False)
    db.commit()
    return "updated"
