from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from transport_agent import TransportAgent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD DATA ----------------
vehicles = pd.read_csv(os.path.join(BASE_DIR, "data", "vehicle_specs.csv"))
fuel = pd.read_csv(os.path.join(BASE_DIR, "data", "fuel_price.csv"))

fuel_price = float(
    fuel[fuel["fuel_type"] == "Diesel"]["price_per_litre_rs"].values[0]
)

# ---------------- INIT AGENT ----------------
agent = TransportAgent(vehicles, fuel_price)


# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Transport Agent API running"}


@app.get("/transport")
def get_transport(quantity: float):
    result = agent.recommend_transport(quantity)
    return result
