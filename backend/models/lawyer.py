from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum


class SubscriptionTier(str, Enum):
    free = "free"
    premium = "premium"
    boosted = "boosted"


class Location(BaseModel):
    address: str
    city: str
    state: str
    pincode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LawyerRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str
    bar_council_id: str
    specializations: List[str]  # e.g. ["Criminal", "Family", "Corporate"]
    experience_years: int
    fee_per_consultation: float
    location: Location
    languages: List[str]  # e.g. ["English", "Tamil", "Hindi"]
    bio: Optional[str] = None
    subscription: SubscriptionTier = SubscriptionTier.free


class LawyerLogin(BaseModel):
    email: EmailStr
    password: str


class LawyerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    specializations: Optional[List[str]] = None
    experience_years: Optional[int] = None
    fee_per_consultation: Optional[float] = None
    location: Optional[Location] = None
    languages: Optional[List[str]] = None
    bio: Optional[str] = None
    subscription: Optional[SubscriptionTier] = None


class RatingInput(BaseModel):
    lawyer_id: str
    client_name: str
    rating: float = Field(..., ge=1, le=5)
    review: Optional[str] = None


class MentorshipInput(BaseModel):
    lawyer_id: str
    student_name: str
    topic: str
    duration_minutes: int


class LawyerSearchQuery(BaseModel):
    city: Optional[str] = None
    specialization: Optional[str] = None
    max_fee: Optional[float] = None
    language: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = 10.0
