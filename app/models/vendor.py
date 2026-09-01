from typing import List
from pydantic import BaseModel


class LocalGuide(BaseModel):
    id: int
    name: str
    region: str
    is_verified: bool
    languages: List[str]
    rating: float
    bio: str


class Homestay(BaseModel):
    id: int
    name: str
    region: str
    is_verified: bool
    sustainability_tags: List[str]
    eco_friendly: bool
    price_per_night: float
    rating: float