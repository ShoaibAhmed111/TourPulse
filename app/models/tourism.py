from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class CrowdStatus(str, Enum):
    LOW = 'Low'
    MODERATE = 'Moderate'
    HIGH = 'High'


class DestinationCreate(BaseModel):
    name: str
    location: str
    description: str
    category: str
    current_visitor_count: int = Field(ge=0)
    max_capacity: int = Field(gt=0)


class Destination(DestinationCreate):
    id: int
    crowd_status: CrowdStatus
    crowd_score: float


class Hotel(BaseModel):
    id: int
    name: str
    destination_id: int
    rating: float
    price_per_night: float


class TourPackage(BaseModel):
    id: int
    title: str
    destination_id: int
    price: float
    duration_days: int


class ItineraryRequest(BaseModel):
    budget: float = Field(gt=0)
    days: int = Field(gt=0, le=14)
    travel_style: str  # e.g., 'relaxed', 'adventure', 'cultural', 'budget'


class DayPlan(BaseModel):
    day: int
    activities: List[str]
    recommended_destination: str
    estimated_cost: float


class ItineraryResponse(BaseModel):
    days_plan: List[DayPlan]
    total_estimated_cost: float
    travel_style: str