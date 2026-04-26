import argparse
import json
import os

FILE = "todos.json"

def load_todos():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_todos(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=2)

def add_task(task):
    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)
    print(f"Added: {task}")

def list_tasks():
    todos = load_todos()
    for i, t in enumerate(todos):
        status = "✓" if t["done"] else " "
        print(f"{i}: [{status}] {t['task']}")

def complete_task(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["done"] = True
        save_todos(todos)
        print("Marked as done")
    else:
        print("Invalid index")

parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("value", nargs="?")

args = parser.parse_args()

if args.command == "add":
    add_task(args.value)
elif args.command == "list":
    list_tasks()
elif args.command == "done":
    complete_task(int(args.value))
