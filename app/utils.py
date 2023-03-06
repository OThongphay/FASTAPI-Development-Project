from passlib.context import CryptContext

#Defines that we are using bycrpt as our library to hash
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

#Returns hashed password in when called from main.py
def hash(password: str):
    return pwd_context.hash(password)

#Used to verify the passwords are the same
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)