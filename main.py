from fastapi import FastAPI
from Routes import Month , Transactions,Users

app = FastAPI( 
    title="Money App",
    description="Budget App for managing expenses and predicting furture expense based on expendeture.",
    version="0.0.1",
    contact={
        "name": "Ahmed Ali",
        "email": "ahmedalibalti2000@gmail.com",
    })

@app.get("/")
def root():
    return {"message": "Hello World "}
app.include_router(Users.router, prefix="/User",tags=["Users"])
app.include_router(Month.router, prefix="/Month",tags=["Months"])
app.include_router(Transactions.router, prefix="/Transactions",tags=["Transactions"])

