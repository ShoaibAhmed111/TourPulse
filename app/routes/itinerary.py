from fastapi import APIRouter, HTTPException, status
from app.models.tourism import ItineraryRequest, ItineraryResponse, DayPlan

router = APIRouter(prefix="/api/itinerary", tags=["itinerary"])


@router.post("/generate", response_model=ItineraryResponse)
def generate_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    if request.days <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be greater than zero."
        )
    if request.budget <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget must be greater than zero."
        )

    destination = getattr(request, "destination", None) or "Tanzania"
    travel_style = (getattr(request, "travel_style", None) or "balanced").lower()
    num_days = request.days
    total_budget = float(request.budget)

    daily_budget = total_budget / num_days

    activities_catalog = {
        "budget": [
            "Explore local markets and taste street food specialties",
            "Self-guided walking tour of historical town landmarks",
            "Relax at scenic public beach or botanical garden",
            "Community-led cultural walk and local craft demonstration",
            "Sunset viewing at a popular vantage point",
            "Visit local artisan cooperatives and markets",
            "Day hike to nearby waterfalls and natural pools"
        ],
        "luxury": [
            "Private morning game drive with exclusive expert guide",
            "Hot air balloon safari with champagne bush breakfast",
            "Private helicopter scenic tour and VIP lodge lunch",
            "Exclusive luxury spa treatment and private beach cabana",
            "Private sunset yacht charter with gourmet catering",
            "Fine dining wine-pairing dinner experience",
            "Fly-in safari experience to remote private reserve"
        ],
        "adventure": [
            "Kilimanjaro or Mount Meru day trek experience",
            "Scuba diving and marine life exploration",
            "Quad biking through scenic rural landscapes",
            "Canoeing safari on Lake Duluti",
            "Night game drive spotting nocturnal wildlife",
            "Ziplining and canopy walking adventure",
            "Guided mountain biking through local coffee plantations"
        ],
        "culture": [
            "Guided historical walking tour of Stone Town",
            "Spice farm tour and interactive traditional cooking class",
            "Maasai village visit and cultural exchange",
            "National museum and cultural heritage site tour",
            "Traditional drum and dance workshop",
            "Historical ruins tour and storytelling session",
            "Artisan craft workshop with local master craftspeople"
        ],
        "safari": [
            "Full day game drive in Serengeti National Park",
            "Ngorongoro Crater floor wildlife tour",
            "Tarangire National Park elephant and baobab safari",
            "Lake Manyara flamingo and tree-climbing lion safari",
            "Guided bush walking safari with professional ranger",
            "Specialized birdwatching and nature walk expedition",
            "Visit wildlife conservation and rehabilitation center"
        ]
    }

    style_key = travel_style if travel_style in activities_catalog else "safari"
    pool = activities_catalog[style_key]

    day_plans = []
    accumulated_cost = 0.0

    for i in range(1, num_days + 1):
        act_idx1 = ((i - 1) * 2) % len(pool)
        act_idx2 = ((i - 1) * 2 + 1) % len(pool)

        day_activities = [
            pool[act_idx1],
            pool[act_idx2],
            f"Evening leisure and dinner themed for {travel_style} travel"
        ]

        cost_multiplier = 0.9 + (i % 3) * 0.1
        if i == num_days:
            day_cost = round(max(0.0, total_budget - accumulated_cost), 2)
        else:
            day_cost = round(min(daily_budget * cost_multiplier, total_budget - accumulated_cost), 2)

        accumulated_cost += day_cost

        day_plan_kwargs = {
            "day": i,
            "title": f"Day {i}: {destination} Highlights",
            "activities": day_activities,
            "estimated_cost": day_cost,
            "description": f"Customized day plan tailored for {travel_style} style in {destination}.",
            "notes": f"Estimated allocation: ${day_cost:.2f}"
        }

        valid_day_fields = getattr(DayPlan, '__fields__', None) or getattr(DayPlan, 'model_fields', None)
        if valid_day_fields:
            filtered_kwargs = {k: v for k, v in day_plan_kwargs.items() if k in valid_day_fields}
            day_plan = DayPlan(**filtered_kwargs)
        else:
            day_plan = DayPlan(**day_plan_kwargs)

        day_plans.append(day_plan)

    response_kwargs = {
        "destination": destination,
        "total_days": num_days,
        "total_estimated_cost": round(accumulated_cost, 2),
        "travel_style": travel_style,
        "day_plans": day_plans,
        "days": day_plans,
        "summary": f"{num_days}-day {travel_style} itinerary for {destination} with a budget of ${total_budget:.2f}."
    }

    valid_resp_fields = getattr(ItineraryResponse, '__fields__', None) or getattr(ItineraryResponse, 'model_fields', None)
    if valid_resp_fields:
        filtered_resp = {k: v for k, v in response_kwargs.items() if k in valid_resp_fields}
        return ItineraryResponse(**filtered_resp)

    return ItineraryResponse(**response_kwargs)