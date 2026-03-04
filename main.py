import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-u","--update",nargs=2,metavar=("ID,TASK"),help="update task information by ID")
parser.add_argument("-p","--priority",nargs=2,metavar=("ID","PRIORITY"),help="Add priority")
parser.add_argument("-dat","--date",nargs=2,metavar=("ID,DATE"),help="update task information by ID")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-v", "--version",action = "version",version= "2.2.1")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
if args.list:
    tasks = load_tasks()
    if len(tasks) == 0:
        print("No tasks left to complete :) ")
    else:
        for task in tasks:
            status = "X" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['task']} {task['due']}")
    sys.exit(0)
elif args.update:
    tasks = load_tasks()
    task_id = int(args.update[0])
    info = args.update[1]
    for task in tasks:
        if task["id"] == task_id:
            task["task"] = info
            save_task(tasks)
            print(f"Task {task_id} updated to add {info}")   
elif args.date:
    tasks = load_tasks()
    task_id = int(args.date[0])
    due_date = args.date[1]
    for task in tasks:
        if task["id"] == task_id:
            task["due"] = due_date
            save_task(tasks)
            print(f"Task {task_id} updated to add date of {due_date}")
elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            task["done"] = True
            save_task(tasks)
            print(f"Task {args.complete} marked as complete")
            break
elif args.delete:
    tasks = load_tasks()
    new_tasks = []
    for task in tasks:
        if task["id"] != args.delete:
            new_tasks.append(task)
    tasks = new_tasks
    save_task(new_tasks)
    print(f"Task with ID of {args.delete} deleted")
elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1
    tasks.append({"id": new_id, "task": args.task, "done": False, "due-date": "04-05-2026", "priority": args.priority})
    save_task(tasks)
    print(f"Task {args.task} added with ID of {new_id}")
elif args.priority:
    tasks = load_tasks()
    task_id = int(args.priority[0])
    priority = args.priority[1]
    if priority not in ["High","Medium","Low"]:
        print("Invalid Priority")
        sys.exit(1)
    for task in tasks:
        if task["id"] == task_id:
            task["priority"] = priority
            save_task(tasks)
            print(f"Task {task_id} updated to add priority of {priority}")