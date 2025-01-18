from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict, Optional


class GroundDetails(BaseModel):
    name: str
    email: str
    latitude: str
    longitude: str
    city: str
    country: str
    address: str
    stadiumtype: str
    sportshours: str
    description: str
    rating: float = None  # Optional
    total_ratings: int = None  # Optional

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
    email: str
    latitude: str
    longitude: str
    city: str
    address: str
    description: str
    stadiumtype: str
    sportshours: str
    rating: Optional[float]
    created_at: datetime
    image: Optional[str]

class GroundUpdate(BaseModel):
    name: str
    email: str
    latitude: str
    longitude: str
    stadiumtype: str
    sportshours: str
    city: str
    address: str
    description: str
    country: str
