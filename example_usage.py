from client import GigWorkerYieldOptimizerClient
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

def main():
    optimizer = GigWorkerYieldOptimizerClient()
    print("=== GIG WORKER MULTI-PLATFORM SHIFT YIELD OPTIMIZER ===")

    # 4-hour evening shift budget
    tasks = [
        {"task_id": "DELIVERY-01", "platform": "DoorDash", "gross_payout": 18.50, "duration_minutes": 30, "travel_distance_km": 4.5},
        {"task_id": "RIDE-02",     "platform": "Uber",     "gross_payout": 34.00, "duration_minutes": 55, "travel_distance_km": 12.0},
        {"task_id": "GROCERY-03",  "platform": "Instacart","gross_payout": 22.00, "duration_minutes": 45, "travel_distance_km": 6.0},
        {"task_id": "EXPRESS-04",  "platform": "DoorDash", "gross_payout": 14.00, "duration_minutes": 20, "travel_distance_km": 2.5},
        {"task_id": "LONG-RIDE-05","platform": "Lyft",     "gross_payout": 48.00, "duration_minutes": 80, "travel_distance_km": 28.0}
    ]

    res = optimizer.optimize_shift(4.0, tasks)
    print()
    print(f"Shift Budget: 4.0 Hours | Work Time: {res['allocated_hours']} Hours ({res['selected_tasks_count']} Tasks)")
    print(f"Total Net Take-Home: ${res['projected_net_earnings']}")
    print(f"Effective Hourly Rate: ${res['effective_hourly_wage']}/hr")
    print()
    print("Optimal Task Dispatch Schedule:")
    for t in res['selected_tasks']:
        print(f"  [{t['platform']:<9}] {t['task_id']}: Net ${t['net_payout']} ({t['duration_minutes']} min, {t['travel_distance_km']} km)")

if __name__ == "__main__":
    main()
