from fastapi import APIRouter, status, HTTPException,Depends
from pydantic_schemas import pydantic_Transactions
from Utils.JWT import get_current_user
from DB.db_setup import get_db
from sqlalchemy.orm import Session
from typing import List
from DB.SQL_Alchemy_Models.Models_Transactions import Transaction

router = APIRouter()
#id of month
@router.post('/Addtransaction/{id}',status_code=status.HTTP_201_CREATED, response_model= pydantic_Transactions.out_transaction)
def create_transactions(id:int,transactions:pydantic_Transactions.Monthly_transaction, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data={**transactions.dict(),"month_id":id}
    new = Transaction(**data)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new
#id of month    
@router.get('/gettransactions/{id}',status_code=status.HTTP_201_CREATED, response_model= List[pydantic_Transactions.out_transaction])
def all_transactions(id:int, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    transactions = db.query(Transaction).filter(Transaction.month_id==id).all()
    return transactions
#id of Transaction    
@router.put('/updatetransactions/{id}',status_code=status.HTTP_201_CREATED, response_model= str)
def update_transactions(id:int,updated:pydantic_Transactions.Monthly_transaction, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)   
    qmonth = db.query(Transaction).filter(Transaction.id==id)
    month=qmonth.first()
    if(month == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    qmonth.update(updated.dict(), synchronize_session=False)
    db.commit()
    return "updated"
#id of Transaction
@router.delete('/deletetransactions/{id}',status_code=status.HTTP_201_CREATED, response_model= str)
def delete_month(id:int,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)   
    qTrans = db.query(Transaction).filter(Transaction.id==id)
    Trans=qTrans.first()
    if(Trans == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    qTrans.delete(synchronize_session=False)
    db.commit()
    return "deleted"
