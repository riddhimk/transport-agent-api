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

    def evaluate_vehicle(self, vehicle_row, load_ton, distance_km):
        capacity = float(vehicle_row["capacity_ton"])
        mileage = float(vehicle_row["mileage_kmpl"])

        cost_per_km = self.compute_cost_per_km(mileage)
        total_cost = cost_per_km * distance_km

        utilization = min(load_ton / capacity, 1)
        cost_per_tonne = total_cost / load_ton

        return {
            "vehicle_type": str(vehicle_row["vehicle_type"]),
            "model": str(vehicle_row["model"]),
            "capacity": capacity,
            "cost_per_km": round(cost_per_km, 2),
            "total_cost": round(total_cost, 2),
            "utilization": round(utilization, 3),
            "cost_per_tonne": round(cost_per_tonne, 2)
        }

    def recommend_transport(self, quantity_kg, distance_km):

        quantity_ton = quantity_kg / 1000

        # -------------------------------
        # CASE 1: SINGLE VEHICLE
        # -------------------------------
        best_single = None

        for _, row in self.vehicle_data.iterrows():
            capacity = float(row["capacity_ton"])

            if quantity_ton <= capacity:
                candidate = self.evaluate_vehicle(row, quantity_ton, distance_km)

                if best_single is None or candidate["cost_per_tonne"] < best_single["cost_per_tonne"]:
                    best_single = candidate

        if best_single is not None:
            return {
                "mode": "single_vehicle",
                "vehicle": best_single,
                "total_cost": best_single["total_cost"]
            }

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