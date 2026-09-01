from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes import crowd_predictor, destinations, itinerary, vendors, concierge

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(destinations.router)
app.include_router(itinerary.router)
app.include_router(crowd_predictor.router, prefix="/api/crowd", tags=["Crowd Predictor"])
app.include_router(vendors.router, prefix="/api/vendors", tags=["Vendors"])
app.include_router(concierge.router, prefix="/api/concierge", tags=["Concierge"])

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")