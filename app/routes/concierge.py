from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    response: str

KNOWLEDGE_BASE = {
    "munnar": "🌿 **Munnar:** Visit the tea estates between 6:30 AM and 9:00 AM to avoid the main tourist buses. Eco-tip: Hire local electric tuk-tuks to navigate the hills and reduce your carbon footprint.",
    "hampi": "🛕 **Hampi:** The ancient ruins are best explored just after sunrise (6:00 AM) or late afternoon (4:00 PM). Please carry a reusable water bottle, as plastic waste severely damages this heritage site.",
    "jaipur": "🏰 **Jaipur:** To beat the crowds at Amber Fort, arrive right at opening time (8:00 AM). Support sustainable tourism by purchasing directly from local block-printing artisans rather than mass-market emporiums.",
    "goa": "🌊 **Goa:** Avoid the congested northern beaches. Head to South Goa (like Palolem) early morning. Choose eco-shacks that use solar power, harvest rainwater, and ban single-use plastics.",
    "varanasi": "🕉️ **Varanasi:** Experience the ghats during a 5:30 AM boat ride to avoid the overwhelming evening Aarti crowds. Always respect the Ganges by never dropping non-biodegradable offerings into the water.",
    "leh": "🏔️ **Leh:** High-altitude lakes like Pangong Tso get crowded by noon; start your drive by 5:00 AM. High-altitude ecosystems are extremely fragile—strictly pack out all your trash."
}

@router.post("/chat", response_model=ChatMessageResponse)
def concierge_chat(payload: ChatMessageRequest):
    msg = payload.message.lower()
    
    for destination, advice in KNOWLEDGE_BASE.items():
        if destination in msg:
            return ChatMessageResponse(response=advice)
            
    return ChatMessageResponse(
        response="I can optimize your itinerary for crowds and sustainability! Ask me about Munnar, Hampi, Jaipur, Goa, Varanasi, or Leh."
    )