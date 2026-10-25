import sys, json
from client import GigWorkerYieldOptimizerClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    optimizer = GigWorkerYieldOptimizerClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "openclaw-genpark-gig-worker"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    hours = req.get("shift_hours_budget", 4.0)
    tasks = req.get("candidate_tasks", [])
    res = optimizer.optimize_shift(hours, tasks)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
