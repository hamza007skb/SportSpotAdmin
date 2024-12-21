from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict, Optional


class GroundDetails(BaseModel):
    name: str
    phone_no: str = '12356789'
    latitude: str
    longitude: str
    city: str
    country: str
    address: str
    description: str
    rating: float = None  # Optional
    total_ratings: int = None  # Optional
    verified_by: str = 'sameer@gmail.com'

class Pitch(BaseModel):
    name: str
    description: str
    length: str
    width: str
    game_type: str
    price_per_60mins: str
    price_per_90mins: str

class PitchUpdate(BaseModel):
    name: str
    description: str
    length: str
    width: str
    game_type: str
    price_per_60mins: str
    price_per_90mins: str

class GroundResponse(BaseModel):
    ground: GroundDetails
    ownerEmail: str
    pitches: List[Pitch]
    facilities: List[str]
    equipments: List[str]
    images: List[str]

class GroundResponseModel(BaseModel):
    id: int
    name: str
    phone_no: str
    latitude: str
    longitude: str
    city: str
    address: str
    description: str
    rating: Optional[float]
    verified_by: str
    created_at: datetime

class GroundUpdate(BaseModel):
    name: str
    phone_no: str
    latitude: str
    longitude: str
    city: str
    address: str
    description: str
    country: str
