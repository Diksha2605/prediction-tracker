from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from backend.models.user import PlanType

class UserRegister(BaseModel):
    name:     str = Field(..., min_length=2, max_length=100)
    email:    EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserOut(BaseModel):
    id:         UUID
    name:       str
    email:      str
    plan:       PlanType
    created_at: datetime
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserOut