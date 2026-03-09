#!/usr/bin/env python3
"""
OPC Project Tracker

用法：
  python3 project_tracker.py init <project_name>
  python3 project_tracker.py add '{"name":"任务","role":"角色"}'
  python3 project_tracker.py update T001 completed 25000
  python3 project_tracker.py show
  python3 project_tracker.py report
"""
import json, sys, os
from datetime import datetime

STATE_FILE = "/tmp/opc_project.json"

def load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return None

def save(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def init(name):
    data = {
        "project": name,
        "created": datetime.now().isoformat(),
        "tasks": [],
        "cost": {"total_tokens": 0, "by_role": {}}
    }
    save(data)
    print(f"Project '{name}' initialized.")

def add_task(task_json):
    data = load()
    if not data:
        print("No project. Run: init <name>")
        return
    task = json.loads(task_json)
    task.setdefault("status", "pending")
    task.setdefault("tokens", 0)
    task["id"] = f"T{len(data['tasks'])+1:03d}"
    data["tasks"].append(task)
    save(data)
    print(f"Added {task['id']}: {task.get('name','')}")

def update_task(task_id, status, tokens=0):
    data = load()
    if not data:
        return
    for t in data["tasks"]:
        if t["id"] == task_id:
            t["status"] = status
            if tokens:
                t["tokens"] = int(tokens)
                role = t.get("role", "unknown")
                data["cost"]["by_role"].setdefault(role, 0)
                data["cost"]["by_role"][role] += int(tokens)
                data["cost"]["total_tokens"] += int(tokens)
            save(data)
            print(f"Updated {task_id} -> {status}")
            return
    print(f"Task {task_id} not found")

def show():
    data = load()
    if not data:
        print("No project.")
        return
    print(f"\nProject: {data['project']}")
    print(f"Created: {data['created']}")
    print(f"\n{'ID':<6} {'Task':<30} {'Role':<15} {'Status':<12} {'Tokens':<8}")
    print("-" * 75)
    for t in data["tasks"]:
        print(f"{t['id']:<6} {t.get('name',''):<30} {t.get('role',''):<15} {t['status']:<12} {t.get('tokens',0):<8}")
    print(f"\nTotal tokens: {data['cost']['total_tokens']:,}")

def report():
    data = load()
    if not data:
        return
    print(f"\n# {data['project']} Cost Report\n")
    print("| Role | Tokens | Cost |")
    print("|------|--------|------|")
    for role, tokens in data["cost"]["by_role"].items():
        cost = tokens * 2.5 / 1_000_000
        print(f"| {role} | {tokens//1000}K | ${cost:.2f} |")
    total = data["cost"]["total_tokens"]
    total_cost = total * 2.5 / 1_000_000
    print(f"| **Total** | **{total//1000}K** | **${total_cost:.2f}** |")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "init" and len(sys.argv) > 2:
        init(sys.argv[2])
    elif cmd == "add" and len(sys.argv) > 2:
        add_task(sys.argv[2])
    elif cmd == "update" and len(sys.argv) > 3:
        tokens = sys.argv[4] if len(sys.argv) > 4 else 0
        update_task(sys.argv[2], sys.argv[3], tokens)
    elif cmd == "show":
        show()
    elif cmd == "report":
        report()
    else:
        print(__doc__)
