from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str  # student | parent | teacher | admin

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str
