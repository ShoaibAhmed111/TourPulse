# app/routes/destinations.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

class DestinationBase(BaseModel):
    name: str
    location: str = "India"
    description: str = "A scenic travel destination."
    category: str = "General"
    current_visitor_count: int = 250
    crowd_score: int = Field(default=50, ge=0, le=100)
    status_tag: str = Field(default="Moderate")
    peak_hours: str = Field(default="10:00 AM - 4:00 PM")
    image_url: str = Field(default="https://images.unsplash.com/photo-1596176530529-78163a4f7af2")
    lat: float = Field(default=20.5937)
    lng: float = Field(default=78.9629)

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int

# In-memory storage seeded with valid records
destinations_db: List[Destination] = [
    Destination(
        id=1,
        name="Munnar Tea Plantations",
        location="Idukki, Kerala",
        description="Lush rolling hills and serene tea estates with misty valleys.",
        category="Nature & Hills",
        current_visitor_count=320,
        crowd_score=28,
        status_tag="Low",
        peak_hours="09:00 AM - 01:00 PM",
        image_url="https://images.unsplash.com/photo-1593693397690-362cb9666fc2",
        lat=10.0889,
        lng=77.0595
    ),
    Destination(
        id=2,
        name="Hampi Monument Complex",
        location="Vijayanagara, Karnataka",
        description="UNESCO World Heritage site with ancient ruins and boulders.",
        category="Heritage & Culture",
        current_visitor_count=580,
        crowd_score=45,
        status_tag="Moderate",
        peak_hours="08:00 AM - 11:30 AM",
        image_url="https://images.unsplash.com/photo-1600100397608-f010e42e47d4",
        lat=15.3350,
        lng=76.4600
    ),
    Destination(
        id=3,
        name="Amber Palace & Fort",
        location="Jaipur, Rajasthan",
        description="Opulent hilltop palace with courtyards and intricate mirror work.",
        category="Historical Fort",
        current_visitor_count=1850,
        crowd_score=88,
        status_tag="High",
        peak_hours="11:00 AM - 04:30 PM",
        image_url="https://images.unsplash.com/photo-1599661046289-e31897846e41",
        lat=26.9855,
        lng=75.8513
    ),
    Destination(
        id=4,
        name="Palolem Eco Coast",
        location="South Goa, Goa",
        description="Crescent beach known for quiet dolphin spots and sustainable shacks.",
        category="Coastal & Beach",
        current_visitor_count=420,
        crowd_score=35,
        status_tag="Low",
        peak_hours="04:00 PM - 07:00 PM",
        image_url="https://images.unsplash.com/photo-1512343879784-a960bf40e7f2",
        lat=15.0100,
        lng=74.0232
    ),
    Destination(
        id=5,
        name="Dashashwamedh Ghat",
        location="Varanasi, Uttar Pradesh",
        description="Historic spiritual ghat famous for the evening Ganga Aarti.",
        category="Spiritual & Pilgrimage",
        current_visitor_count=2400,
        crowd_score=94,
        status_tag="High",
        peak_hours="05:30 PM - 08:30 PM",
        image_url="https://images.unsplash.com/photo-1561361513-2d000a50f0dc",
        lat=25.3076,
        lng=83.0107
    ),
    Destination(
        id=6,
        name="Pangong Tso & Leh Valley",
        location="Leh, Ladakh",
        description="High-altitude azure salt lake surrounded by barren peaks.",
        category="Adventure & Mountain",
        current_visitor_count=210,
        crowd_score=22,
        status_tag="Low",
        peak_hours="10:00 AM - 02:00 PM",
        image_url="https://images.unsplash.com/photo-1581793745862-99fde7fa73d2",
        lat=34.1526,
        lng=77.5771
    )
]

@router.get("/", response_model=List[Destination])
def get_destinations():
    return destinations_db

@router.get("/{dest_id}", response_model=Destination)
def get_destination(dest_id: int):
    for d in destinations_db:
        if d.id == dest_id:
            return d
    raise HTTPException(status_code=404, detail="Destination not found")

@router.post("/", response_model=Destination)
def create_destination(payload: DestinationCreate):
    new_id = max([d.id for d in destinations_db], default=0) + 1
    new_dest = Destination(id=new_id, **payload.model_dump())
    destinations_db.append(new_dest)
    return new_dest