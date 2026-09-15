from __future__ import annotations

import asyncio
import contextlib
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import concierge, crowd_predictor, destinations, itinerary, vendors
from app.services.telemetry import CrowdTelemetryEngine

app = FastAPI(title="TourPulse", version="2.0.0", description="Smart tourism, crowd balancing and local economy platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Internal consistency in endpoint routes
app.include_router(destinations.router, prefix="/api/destinations")
app.include_router(itinerary.router, prefix="/api/itinerary")
app.include_router(crowd_predictor.router, prefix="/api/crowd")
app.include_router(vendors.router, prefix="/api/vendors")
app.include_router(concierge.router, prefix="/api/concierge")

@app.get("/api/alternatives/{dest_id}")
def get_alternatives(dest_id: int):
    destination = next((d for d in destinations.destinations_db if d.id == dest_id), None)
    if destination is None:
        return {"source": None, "alternatives": []}
    alternatives = []
    for alt_id in destination.alternate_ids:
        alt = next((d for d in destinations.destinations_db if d.id == alt_id), None)
        if not alt:
            continue
        alternatives.append({
            "destination": alt.model_dump(),
            "reason": f"{alt.name} is {max(0, int(destination.crowd_score - alt.crowd_score))}% lower on crowd pressure.",
            "crowd_reduction": max(0, int(destination.crowd_score - alt.crowd_score)),
            "distance_km": 12.0 + alt.id,
            "local_economy_score": min(98, 68 + alt.id * 2),
        })
    alternatives.sort(key=lambda x: (x["destination"]["crowd_score"], -x["local_economy_score"]))
    return {"source": destination.model_dump(), "alternatives": alternatives}

@app.get("/api/impact/summary")
def get_impact_summary():
    high_alerts = sum(1 for d in destinations.destinations_db if d.crowd_score > 75)
    return {
        "projected_crowd_reduction": 24,
        "projected_secondary_footfall_increase": 18,
        "local_spend_redistributed": 243500.0,
        "businesses_surfaced": len(vendors.MOCK_GUIDES) + len(vendors.MOCK_HOMESTAYS) + len(vendors.MOCK_HOTELS) + len(vendors.MOCK_ARTISANS) + len(vendors.MOCK_EATERIES),
        "high_alerts": high_alerts,
        "destinations_monitored": len(destinations.destinations_db),
    }



# ---------------------------------------------------------------------------
# Live Data Streaming (Stage 4 of the architecture): crowd telemetry is
# recomputed on a fixed interval and pushed to every connected client over a
# WebSocket, so the map reflects congestion building and clearing in real
# time rather than a static snapshot taken at page load.
# ---------------------------------------------------------------------------

PULSE_INTERVAL_SECONDS = 5.0

telemetry_engine = CrowdTelemetryEngine(destinations.destinations_db)


class PulseHub:
    """Tracks connected dashboard clients and fans telemetry out to them."""

    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._clients.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._clients.discard(websocket)

    @property
    def client_count(self) -> int:
        return len(self._clients)

    async def broadcast(self, payload: dict) -> None:
        async with self._lock:
            targets = list(self._clients)
        dead = []
        for client in targets:
            try:
                await client.send_json(payload)
            except Exception:
                # A client that vanished mid-send must not stop the rest of
                # the fan-out, and must not linger in the set forever.
                dead.append(client)
        if dead:
            async with self._lock:
                for client in dead:
                    self._clients.discard(client)


pulse_hub = PulseHub()


def build_pulse_payload() -> dict:
    updates = telemetry_engine.tick(destinations.destinations_db)
    high = [u for u in updates if u.status_tag == "High"]
    return {
        "type": "pulse",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "high_alerts": len(high),
        "destinations": [
            {
                "id": u.id,
                "crowd_score": u.crowd_score,
                "current_visitor_count": u.current_visitor_count,
                "status_tag": u.status_tag,
                "delta": u.delta,
            }
            for u in updates
        ],
    }


async def _pulse_loop() -> None:
    while True:
        await asyncio.sleep(PULSE_INTERVAL_SECONDS)
        if pulse_hub.client_count == 0:
            # No dashboards open -- skip the tick entirely so the demo data
            # isn't drifting in the background with nobody watching.
            continue
        try:
            await pulse_hub.broadcast(build_pulse_payload())
        except Exception:
            # The streaming loop must survive a bad tick; losing it would
            # silently kill live updates for the whole server.
            pass


@app.on_event("startup")
async def _start_pulse() -> None:
    app.state.pulse_task = asyncio.create_task(_pulse_loop())


@app.on_event("shutdown")
async def _stop_pulse() -> None:
    task = getattr(app.state, "pulse_task", None)
    if task:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task


@app.websocket("/ws/pulse")
async def pulse_socket(websocket: WebSocket) -> None:
    await pulse_hub.connect(websocket)
    try:
        # Send an immediate snapshot so a newly opened dashboard doesn't wait
        # a full interval before showing live data.
        await websocket.send_json(build_pulse_payload())
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        await pulse_hub.disconnect(websocket)


@app.get("/api/pulse/snapshot")
def pulse_snapshot():
    """Polling fallback for clients that cannot hold a WebSocket open."""
    return build_pulse_payload()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "TourPulse", "version": "2.0.0"}

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")
