from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    acess_token: str
    token_type: str = "bearer"

class LoginData(BaseModel):
    email: EmailStr
    password: str