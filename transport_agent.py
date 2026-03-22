import pandas as pd
import math


class TransportAgent:

    def __init__(self, vehicle_data, fuel_price):
        self.vehicle_data = vehicle_data
        self.fuel_price = fuel_price

    def compute_cost_per_km(self, mileage):
        fuel_cost = self.fuel_price / mileage
        overhead = 3
        return fuel_cost + overhead

    def evaluate_vehicle(self, vehicle_row, load_ton):
        capacity = float(vehicle_row["capacity_ton"])
        mileage = float(vehicle_row["mileage_kmpl"])
    
        cost_per_km = self.compute_cost_per_km(mileage)
    
        # 🔥 CORE CHANGE
        cost_per_tonne_per_km = cost_per_km / capacity
    
        return {
            "vehicle_type": str(vehicle_row["vehicle_type"]),
            "model": str(vehicle_row["model"]),
            "capacity": capacity,
            "mileage": mileage,
            "cost_per_tonne_per_km": round(cost_per_tonne_per_km, 3)
        }

    def recommend_transport(self, quantity_kg):

        quantity_ton = quantity_kg / 1000

        # -------------------------------
        # CASE 1: SINGLE VEHICLE
        # -------------------------------
        best_single = None

        for _, row in self.vehicle_data.iterrows():
            candidate = self.evaluate_vehicle(row, quantity_ton)

            if quantity_ton <= capacity:
                candidate = self.evaluate_vehicle(row, quantity_ton, distance_km)

                if best is None or candidate["cost_per_tonne_per_km"] < best["cost_per_tonne_per_km"]:
                    best = candidate

        if best_single is not None:
            return best

        # -------------------------------
        # CASE 2: MULTIPLE VEHICLES
        # -------------------------------
        remaining_load = quantity_ton
        selected_vehicles = []

        sorted_vehicles = self.vehicle_data.sort_values(by="capacity_ton", ascending=False)

        while remaining_load > 0:

            best_option = None

            for _, row in sorted_vehicles.iterrows():
                capacity = float(row["capacity_ton"])
                load = min(capacity, remaining_load)

                candidate = self.evaluate_vehicle(row, load, distance_km)

                if best_option is None or candidate["cost_per_tonne"] < best_option["cost_per_tonne"]:
                    best_option = candidate

            selected_vehicles.append(best_option)
            remaining_load -= best_option["capacity"]

        total_cost = round(sum(v["total_cost"] for v in selected_vehicles), 2)

        return {
            "mode": "multiple_vehicles",
            "vehicles_used": len(selected_vehicles),
            "vehicle_plan": selected_vehicles,
            "total_cost": total_cost
        }
