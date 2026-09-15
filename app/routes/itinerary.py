from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.tourism import DayPlan, ItineraryRequest, ItineraryResponse
from app.routes.destinations import destinations_db

router = APIRouter(tags=["Smart Itinerary"])

STYLE_POOLS = {
    "balanced": [
        "Sunrise viewpoint and quiet local breakfast",
        "Guided heritage or nature walk",
        "Community-run lunch experience",
        "Flexible free time at a low-density attraction",
        "Sunset photography stop",
    ],
    "nature": [
        "Early forest or tea-estate walk",
        "Birding and landscape viewpoint",
        "Locally guided nature experience",
        "Slow lunch using seasonal produce",
        "Golden-hour scenic trail",
    ],
    "culture": [
        "Sunrise heritage walk",
        "Local museum or architecture circuit",
        "Craft demonstration with a local maker",
        "Traditional regional meal",
        "Storytelling or cultural performance",
    ],
    "adventure": [
        "Early mountain or coastal excursion",
        "Guided active experience",
        "Local recovery lunch",
        "Hidden-gem exploration",
        "Sunset ridge or shoreline session",
    ],
    "budget": [
        "Self-guided early walk",
        "Local market breakfast",
        "Community attraction visit",
        "Street-food or family-run lunch",
        "Free sunset viewpoint",
    ],
}


def _resolve_anchor(destination_name: str):
    name = destination_name.lower()
    exact = next((d for d in destinations_db if d.name.lower() == name), None)
    if exact:
        return exact
    partial = next((d for d in destinations_db if name in d.name.lower() or name in d.location.lower()), None)
    return partial or destinations_db[0]


def _pick_destinations(anchor, avoid_high_crowd: bool):
    candidates = [anchor]
    alternatives = [d for d in destinations_db if d.id in anchor.alternate_ids]
    if avoid_high_crowd:
        alternatives.sort(key=lambda d: d.crowd_score)
    candidates.extend(alternatives[:2])
    return candidates


@router.post("/generate", response_model=ItineraryResponse)
def generate_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    anchor = _resolve_anchor(request.destination)
    style = request.travel_style.lower()
    if style not in STYLE_POOLS:
        style = "balanced"

    destinations = _pick_destinations(anchor, request.avoid_high_crowd)
    pool = STYLE_POOLS[style]
    daily_budget = request.budget / request.days
    day_plans: list[DayPlan] = []
    notes: list[str] = []

    if anchor.crowd_score > 75 and request.avoid_high_crowd and len(destinations) > 1:
        notes.append(f"{anchor.name} is currently at {anchor.crowd_score:.0f}% crowd score, so lower-density alternatives were prioritized.")
    else:
        notes.append("The plan favors early starts and locally owned experiences to spread spending beyond major hotspots.")

    for day in range(1, request.days + 1):
        target = destinations[(day - 1) % len(destinations)]
        if target.crowd_score > 75:
            time_note = f"Schedule {target.name} in its quieter window: {target.best_time}."
        else:
            time_note = f"Best window: {target.best_time}."
        activities = [pool[(day * 2 + i) % len(pool)] for i in range(3)]
        cost = round(min(daily_budget * (0.88 + 0.06 * (day % 3)), max(0.0, request.budget - sum(p.estimated_cost for p in day_plans))), 2)
        day_plans.append(
            DayPlan(
                day=day,
                title=f"Day {day} · {target.name}",
                recommended_destination=target.name,
                activities=activities,
                estimated_cost=cost,
                crowd_note=f"Crowd score {target.crowd_score:.0f}/100 · {target.status_tag}. {time_note}",
                sustainability_tip="Choose local operators, refill water, and avoid single-use plastics on the route.",
            )
        )

    total = round(sum(p.estimated_cost for p in day_plans), 2)
    return ItineraryResponse(
        destination=anchor.location,
        total_days=request.days,
        days_plan=day_plans,
        total_estimated_cost=total,
        travel_style=style,
        summary=f"A {request.days}-day {style} route centered on {anchor.location}, optimized around crowd pressure and local experiences.",
        optimization_notes=notes,
    )
