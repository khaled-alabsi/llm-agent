#!/usr/bin/env python3
"""
Minimal CLI Todo Tracker

Usage:
    python main.py add "Todo item"
    python main.py list
    python main.py complete <id>
    python main.py delete <id>
"""

import json
import sys
import os
from datetime import datetime

TODO_FILE = "todos.json"

def load_todos():
    """Load todos from JSON file"""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def add_todo(item):
    """Add a new todo item"""
    todos = load_todos()
    
    new_todo = {
        "id": len(todos) + 1,
        "item": item,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    save_todos(todos)
    print(f"Added todo: {item}")

def list_todos():
    """List all todos"""
    todos = load_todos()
    
    if not todos:
        print("No todos found.")
        return
    
    print("Todos:")
    for todo in todos:
        status = "✓" if todo["completed"] else "○"
        print(f"  [{status}] {todo['id']}: {todo['item']}")

def complete_todo(todo_id):
    """Mark a todo as completed"""
    todos = load_todos()
    
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = True
            save_todos(todos)
            print(f"Completed todo {todo_id}: {todo['item']}")
            return
    
    print(f"Todo with id {todo_id} not found.")

def delete_todo(todo_id):
    """Delete a todo"""
    todos = load_todos()
    
    # Filter out the todo with matching ID
    new_todos = [todo for todo in todos if todo["id"] != todo_id]
    
    if len(new_todos) < len(todos):
        save_todos(new_todos)
        print(f"Deleted todo {todo_id}")
    else:
        print(f"Todo with id {todo_id} not found.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py add \"Todo item\"")
        print("  python main.py list")
        print("  python main.py complete <id>")
        print("  python main.py delete <id>")
        return
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a todo item")
            return
        item = sys.argv[2]
        add_todo(item)
    
    elif command == "list":
        list_todos()
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Please provide todo ID")
            return
        try:
            todo_id = int(sys.argv[2])
            complete_todo(todo_id)
        except ValueError:
            print("Please provide a valid todo ID")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide todo ID")
            return
        try:
            todo_id = int(sys.argv[2])
            delete_todo(todo_id)
        except ValueError:
            print("Please provide a valid todo ID")
    
    else:
        print(f"Unknown command: {command}")
        print("Usage:")
        print("  python main.py add \"Todo item\"")
        print("  python main.py list")
        print("  python main.py complete <id>")
        print("  python main.py delete <id>")

if __name__ == "__main__":
    main()