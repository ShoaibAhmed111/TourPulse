from datetime import datetime, timedelta
from enum import Enum
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CrowdStatus(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"


class CrowdPredictionRequest(BaseModel):
    destination_id: int
    target_time: datetime


class OffPeakSlot(BaseModel):
    recommended_time: datetime
    predicted_crowd_score: float


class CrowdPredictionResponse(BaseModel):
    destination_id: int
    peak_crowd_score: float
    crowd_status: CrowdStatus
    off_peak_slots: List[OffPeakSlot]


def _calculate_score(destination_id: int, dt: datetime) -> float:
    hour = dt.hour
    weekday = dt.weekday()

    # Hourly curve peaking around 13:30
    hour_factor = max(0.0, 1.0 - abs(hour - 13.5) / 7.5)

    # Weekend multiplier
    weekend_factor = 1.3 if weekday in (5, 6) else 1.0

    # Destination-specific offset variation
    dest_factor = 0.8 + ((destination_id * 17) % 40) / 100.0

    raw_score = hour_factor * 80.0 * weekend_factor * dest_factor + 10.0
    return round(max(5.0, min(98.0, raw_score)), 2)


def predict_crowd(request: CrowdPredictionRequest) -> CrowdPredictionResponse:
    target_score = _calculate_score(request.destination_id, request.target_time)

    if target_score < 35.0:
        status = CrowdStatus.LOW
    elif target_score < 65.0:
        status = CrowdStatus.MODERATE
    elif target_score < 85.0:
        status = CrowdStatus.HIGH
    else:
        status = CrowdStatus.VERY_HIGH

    candidates = []
    for hour_offset in range(-8, 9):
        if hour_offset == 0:
            continue
        candidate_time = request.target_time + timedelta(hours=hour_offset)
        if 7 <= candidate_time.hour <= 20:
            score = _calculate_score(request.destination_id, candidate_time)
            if score < target_score:
                candidates.append((score, candidate_time))

    candidates.sort(key=lambda x: (x[0], abs((x[1] - request.target_time).total_seconds())))

    off_peak_slots = [
        OffPeakSlot(recommended_time=dt, predicted_crowd_score=score)
        for score, dt in candidates[:3]
    ]

    return CrowdPredictionResponse(
        destination_id=request.destination_id,
        peak_crowd_score=target_score,
        crowd_status=status,
        off_peak_slots=off_peak_slots,
    )


@router.post("/api/crowd/predict", response_model=CrowdPredictionResponse)
@router.post("/predict", response_model=CrowdPredictionResponse)
def predict_crowd_endpoint(request: CrowdPredictionRequest) -> CrowdPredictionResponse:
    return predict_crowd(request)