from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = ""
    phone: str = ""
    country: str = ""
    referral_code: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ReferralCheckResponse(BaseModel):
    valid: bool
    full_name: str | None = None
    country: str | None = None