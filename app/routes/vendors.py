from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.vendor import Artisan, Hotel, Homestay, LocalEatery, LocalGuide

router = APIRouter(tags=["Local Economy"])


MOCK_GUIDES: List[LocalGuide] = [
    LocalGuide(id="g1", name="Maya Sharma", region="Munnar", destination_ids=[1, 7, 8], languages=["English", "Hindi", "Malayalam"], rating=4.9, bio="Botany educator who specializes in tea landscapes and low-impact forest walks.", specialties=["Nature walks", "Tea culture", "Birding"]),
    LocalGuide(id="g2", name="Ravi Kulkarni", region="Hampi", destination_ids=[2, 9], languages=["English", "Hindi", "Kannada"], rating=4.8, bio="Heritage storyteller connecting visitors with village craft communities around Hampi.", specialties=["Heritage", "Architecture", "Village life"]),
    LocalGuide(id="g3", name="Aarav Mehta", region="Jaipur", destination_ids=[3, 10, 11], languages=["English", "Hindi", "Rajasthani"], rating=4.9, bio="Local historian who focuses on crafts, stepwells and quieter heritage routes.", specialties=["History", "Crafts", "Photography"]),
    LocalGuide(id="g4", name="Nandini Rao", region="Varanasi", destination_ids=[5, 13, 14], languages=["English", "Hindi", "Bhojpuri"], rating=4.7, bio="Cultural guide designing respectful riverfront and artisan experiences away from peak congestion.", specialties=["Culture", "Textiles", "Food"]),
    LocalGuide(id="g5", name="Tashi Namgyal", region="Ladakh", destination_ids=[6, 15], languages=["English", "Hindi", "Ladakhi"], rating=5.0, bio="High-altitude guide with a focus on village homestays and responsible mountain travel.", specialties=["Mountains", "Monasteries", "Sustainability"]),
]

MOCK_HOMESTAYS: List[Homestay] = [
    Homestay(id="h1", name="Misty Valley Eco Stay", region="Munnar", destination_ids=[1, 7, 8], price_per_night=62, amenities=["Solar Power", "Farm Breakfast", "Filtered Water"], rating=4.9),
    Homestay(id="h2", name="Anegundi Courtyard Home", region="Hampi", destination_ids=[2, 9], price_per_night=48, amenities=["Village Kitchen", "Bicycles", "Courtyard"], rating=4.8),
    Homestay(id="h3", name="Sanganer Artisan Home", region="Jaipur", destination_ids=[3, 10, 11], price_per_night=55, amenities=["Craft Studio", "Local Breakfast", "Rooftop"], rating=4.7),
    Homestay(id="h4", name="Agonda Sea Garden", region="South Goa", destination_ids=[4, 12], price_per_night=68, amenities=["Rainwater Harvesting", "Walk to Beach", "Cycle Hire"], rating=4.8),
    Homestay(id="h5", name="Ganges Loom House", region="Varanasi", destination_ids=[5, 13, 14], price_per_night=44, amenities=["Handloom Studio", "Vegetarian Meals", "Courtyard"], rating=4.7),
    Homestay(id="h6", name="Sham Valley Farmstay", region="Ladakh", destination_ids=[6, 15], price_per_night=72, amenities=["Solar Hot Water", "Organic Meals", "Village Walks"], rating=4.9),
]

MOCK_HOTELS: List[Hotel] = [
    Hotel(id="ht1", name="Tea Grove Retreat", region="Munnar", destination_ids=[1, 7, 8], rating=4.8, price_per_night=96, amenities=["Valley View", "Breakfast", "EV Parking"], badge="Local Pick"),
    Hotel(id="ht2", name="Hampi Riverside House", region="Hampi", destination_ids=[2, 9], rating=4.6, price_per_night=82, amenities=["River View", "Pool", "Breakfast"], badge="Near Hidden Gem"),
    Hotel(id="ht3", name="Pink City Courtyard", region="Jaipur", destination_ids=[3, 10, 11], rating=4.7, price_per_night=110, amenities=["Courtyard", "Restaurant", "Guide Desk"], badge="Verified Stay"),
    Hotel(id="ht4", name="Agonda Coast Lodge", region="South Goa", destination_ids=[4, 12], rating=4.8, price_per_night=88, amenities=["Beach Access", "Solar Power", "Yoga Deck"], badge="Eco Stay"),
    Hotel(id="ht5", name="Riverlight Residency", region="Varanasi", destination_ids=[5, 13, 14], rating=4.5, price_per_night=78, amenities=["River View", "Breakfast", "Airport Pickup"], badge="Smart Choice"),
    Hotel(id="ht6", name="Leh Mountain House", region="Ladakh", destination_ids=[6, 15], rating=4.9, price_per_night=125, amenities=["Mountain View", "Solar Heating", "Local Kitchen"], badge="Sustainable"),
]

MOCK_ARTISANS: List[Artisan] = [
    Artisan(id="a1", name="Marayoor Weavers Collective", region="Munnar", destination_ids=[8], craft="Handwoven textiles", price_from=18, rating=4.9, community_story="A women-led cooperative connecting visitors directly with local craft households."),
    Artisan(id="a2", name="Anegundi Bell Metal Studio", region="Hampi", destination_ids=[9], craft="Bell metal craft", price_from=12, rating=4.8, community_story="Small family workshop preserving a traditional metalworking practice."),
    Artisan(id="a3", name="Sanganer Block Print Lab", region="Jaipur", destination_ids=[11], craft="Block printing", price_from=15, rating=4.9, community_story="Visitor workshops support printers and apprentices in a long-running craft quarter."),
    Artisan(id="a4", name="Ramnagar Loom House", region="Varanasi", destination_ids=[14], craft="Handloom textiles", price_from=20, rating=4.8, community_story="Direct-from-maker shopping that keeps more value within the weaving community."),
]

MOCK_EATERIES: List[LocalEatery] = [
    LocalEatery(id="e1", name="Cardamom Table", region="Munnar", destination_ids=[1, 8], cuisine="Kerala mountain cuisine", price_band="₹₹", rating=4.8, signature="Pepper-roasted jackfruit", sustainability_note="Seasonal produce sourced from nearby growers."),
    LocalEatery(id="e2", name="Riverside Thali House", region="Hampi", destination_ids=[2, 9], cuisine="Karnataka vegetarian", price_band="₹", rating=4.7, signature="Local millet thali", sustainability_note="Reusable steel service and village-sourced grains."),
    LocalEatery(id="e3", name="Blue Pot Kitchen", region="Jaipur", destination_ids=[10, 11], cuisine="Rajasthani", price_band="₹₹", rating=4.9, signature="Bajra roti & ker sangri", sustainability_note="Community kitchen model with zero single-use plastic."),
    LocalEatery(id="e4", name="Kashi Courtyard", region="Varanasi", destination_ids=[13, 14], cuisine="North Indian", price_band="₹₹", rating=4.8, signature="Banarasi tamatar chaat", sustainability_note="Local ingredient sourcing and small-batch cooking."),
]


def _filter(items, region: Optional[str], destination_id: Optional[int]):
    filtered = items
    if region:
        filtered = [item for item in filtered if item.region.lower() == region.lower()]
    if destination_id:
        filtered = [item for item in filtered if destination_id in item.destination_ids]
    return filtered


@router.get("/guides", response_model=List[LocalGuide])
def get_local_guides(region: Optional[str] = Query(None), destination_id: Optional[int] = Query(None), verified_only: bool = True):
    items = _filter(MOCK_GUIDES, region, destination_id)
    return [g for g in items if g.is_verified] if verified_only else items


@router.get("/homestays", response_model=List[Homestay])
def get_homestays(region: Optional[str] = Query(None), destination_id: Optional[int] = Query(None), eco_only: bool = True):
    items = _filter(MOCK_HOMESTAYS, region, destination_id)
    return [h for h in items if h.is_eco_friendly] if eco_only else items


@router.get("/hotels", response_model=List[Hotel])
def get_hotels(region: Optional[str] = Query(None), destination_id: Optional[int] = Query(None)):
    items = _filter(MOCK_HOTELS, region, destination_id)
    return [h for h in items if h.is_verified]


@router.get("/artisans", response_model=List[Artisan])
def get_artisans(region: Optional[str] = Query(None), destination_id: Optional[int] = Query(None)):
    items = _filter(MOCK_ARTISANS, region, destination_id)
    return [a for a in items if a.is_verified]


@router.get("/eateries", response_model=List[LocalEatery])
def get_eateries(region: Optional[str] = Query(None), destination_id: Optional[int] = Query(None)):
    items = _filter(MOCK_EATERIES, region, destination_id)
    return [e for e in items if e.is_verified]
