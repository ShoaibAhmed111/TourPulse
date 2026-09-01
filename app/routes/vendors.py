from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()

class LocalGuide(BaseModel):
    id: str
    name: str
    region: str
    is_verified: bool
    languages: List[str] = []
    rating: float = 5.0
    bio: Optional[str] = None

class Homestay(BaseModel):
    id: str
    name: str
    region: str
    is_eco_friendly: bool
    price_per_night: float
    amenities: List[str] = []
    rating: float = 5.0

MOCK_GUIDES: List[LocalGuide] = [
    LocalGuide(
        id="g1",
        name="Tenzin Norbu",
        region="Himalayas",
        is_verified=True,
        languages=["English", "Tibetan", "Hindi"],
        rating=4.9,
        bio="Experienced mountain trekker with 10+ years guiding high altitude trails.",
    ),
    LocalGuide(
        id="g2",
        name="Maya Sharma",
        region="Western Ghats",
        is_verified=True,
        languages=["English", "Kannada", "Hindi"],
        rating=4.8,
        bio="Botany expert specializing in rainforest biodiversity and wildlife spotting.",
    ),
    LocalGuide(
        id="g3",
        name="Lucas Silva",
        region="Amazon Basin",
        is_verified=True,
        languages=["Portuguese", "Spanish"],
        rating=4.2,
        bio="Local river excursion enthusiast.",
    ),
    LocalGuide(
        id="g4",
        name="Samantha Patel",
        region="Himalayas",
        is_verified=True,
        languages=["English", "Nepali"],
        rating=4.7,
        bio="Cultural heritage guide with a passion for storytelling.",
    ),
]

MOCK_HOMESTAYS: List[Homestay] = [
    Homestay(
        id="h1",
        name="Green Valley Eco Lodge",
        region="Himalayas",
        is_eco_friendly=True,
        price_per_night=85.0,
        amenities=["Solar Power", "Organic Farm", "Wifi"],
        rating=4.9,
    ),
    Homestay(
        id="h2",
        name="Rainforest Canopy Retreat",
        region="Western Ghats",
        is_eco_friendly=True,
        price_per_night=60.0,
        amenities=["Rainwater Harvesting", "Guided Walks", "Zero Waste Kitchen"],
        rating=4.7,
    ),
    Homestay(
        id="h3",
        name="Standard Haven Inn",
        region="Amazon Basin",
        is_eco_friendly=False,
        price_per_night=110.0,
        amenities=["Air Conditioning", "Pool", "Wifi"],
        rating=4.0,
    ),
    Homestay(
        id="h4",
        name="Eco Leaf Lodge",
        region="Himalayas",
        is_eco_friendly=True,
        price_per_night=95.0,
        amenities=["Hydroponic Gardens", "Community Support", "Vegetarian Meals"],
        rating=4.8,
    ),
]

@router.get("/guides", response_model=List[LocalGuide])
def get_local_guides(
    region: Optional[str] = Query(None), verified_only: bool = True
) -> List[LocalGuide]:
    guides = MOCK_GUIDES
    if region:
        guides = [g for g in guides if g.region.lower() == region.lower()]
    if verified_only:
        guides = [g for g in guides if g.is_verified]
    return guides

@router.get("/homestays", response_model=List[Homestay])
def get_homestays(
    region: Optional[str] = Query(None), eco_only: bool = True
) -> List[Homestay]:
    homestays = MOCK_HOMESTAYS
    if region:
        homestays = [h for h in homestays if h.region.lower() == region.lower()]
    if eco_only:
        homestays = [h for h in homestays if h.is_eco_friendly]
    return homestays