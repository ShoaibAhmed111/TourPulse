from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class VendorBase(BaseModel):
    id: str
    name: str
    region: str
    destination_ids: List[int] = Field(default_factory=list)
    rating: float = 5.0


class LocalGuide(VendorBase):
    is_verified: bool = True
    languages: List[str] = Field(default_factory=list)
    bio: str = ""
    specialties: List[str] = Field(default_factory=list)


class Homestay(VendorBase):
    is_verified: bool = True
    is_eco_friendly: bool = True
    price_per_night: float
    amenities: List[str] = Field(default_factory=list)


class Hotel(VendorBase):
    is_verified: bool = True
    price_per_night: float
    amenities: List[str] = Field(default_factory=list)
    is_bookable: bool = True
    badge: Optional[str] = None


class Artisan(VendorBase):
    craft: str
    price_from: float
    is_verified: bool = True
    community_story: str


class LocalEatery(BaseModel):
    id: str
    name: str
    region: str
    destination_ids: List[int] = Field(default_factory=list)
    cuisine: str
    price_band: str
    rating: float
    signature: str
    sustainability_note: str
    is_verified: bool = True
