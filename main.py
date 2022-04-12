from fastapi import FastAPI
from Routes import Month , Transactions,Users
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI( 
    title="Money App",
    description="Budget App for managing expenses and predicting furture expense based on expendeture.",
    version="0.0.1",
    contact={
        "name": "Ahmed Ali",
        "email": "ahmedalibalti2000@gmail.com",
    })
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Hello World "}
app.include_router(Users.router, prefix="/User",tags=["Users"])
app.include_router(Month.router, prefix="/Month",tags=["Months"])
app.include_router(Transactions.router, prefix="/Transactions",tags=["Transactions"])

