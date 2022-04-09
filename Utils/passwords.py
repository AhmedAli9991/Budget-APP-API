from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd.hash(password)


def verify(unhashed_password, hashed_password):
    return pwd.verify(unhashed_password, hashed_password)