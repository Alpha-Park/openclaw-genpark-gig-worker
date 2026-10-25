import sys
sys.stdout.reconfigure(encoding='utf-8')

class GigWorkerYieldOptimizerClient:
    """
    Multi-platform gig economy dynamic task allocation engine.
    Solves time-constrained task selection maximizing net hourly take-home pay
    while accounting for pickup travel friction and platform commission deductions.
    """
    def __init__(self, hourly_fuel_cost=3.50):
        self.hourly_fuel_cost = hourly_fuel_cost

    def optimize_shift(self, shift_hours_budget, candidate_tasks):
        """
        candidate_tasks: list of dicts:
        {"task_id": str, "platform": str, "gross_payout": float, "duration_minutes": float, "travel_distance_km": float}
        """
        if not candidate_tasks:
            return {"status": "error", "message": "No tasks provided"}

        minutes_budget = shift_hours_budget * 60.0

        # Calculate effective net yield per task: Net = Gross - fuel (approx $0.15/km)
        scored_tasks = []
        for t in candidate_tasks:
            fuel_cost = float(t.get("travel_distance_km", 0.0)) * 0.15
            net_payout = max(0.0, float(t["gross_payout"]) - fuel_cost)
            dur = max(1.0, float(t["duration_minutes"]))
            yield_per_min = net_payout / dur
            scored_tasks.append({
                **t,
                "net_payout": round(net_payout, 2),
                "yield_per_min": yield_per_min
            })

        # Greedy knapsack heuristic by yield efficiency
        scored_tasks.sort(key=lambda x: x["yield_per_min"], reverse=True)

        selected_tasks = []
        total_time_min = 0.0
        total_net_earnings = 0.0

        for t in scored_tasks:
            if total_time_min + t["duration_minutes"] <= minutes_budget:
                selected_tasks.append(t)
                total_time_min += t["duration_minutes"]
                total_net_earnings += t["net_payout"]

        hours_worked = total_time_min / 60.0
        effective_hourly_wage = (total_net_earnings / hours_worked) if hours_worked > 0 else 0.0

        return {
            "status": "success",
            "shift_hours_budget": shift_hours_budget,
            "allocated_hours": round(hours_worked, 2),
            "selected_tasks_count": len(selected_tasks),
            "projected_net_earnings": round(total_net_earnings, 2),
            "effective_hourly_wage": round(effective_hourly_wage, 2),
            "selected_tasks": selected_tasks
        }
