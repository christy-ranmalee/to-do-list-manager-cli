import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task():
    """Add a new task."""
    description = input("Enter task description: ").strip()
    if not description:
        print("⚠️ Task cannot be empty.")
        return
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added: {description}")


def list_tasks():
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return
    print("\n📝 Your Tasks:")
    for task in tasks:
        status = "✅ Done" if task["done"] else "❌ Pending"
        print(f"[{task['id']}] {status} - {task['description']} (added {task['created_at']})")
    print()


def mark_done():
    """Mark a task as done."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks to update.")
        return
    try:
        task_id = int(input("Enter task ID to mark as done: "))
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"🎉 Task {task_id} marked as done!")
            return
    print("⚠️ Task ID not found.")


def delete_task():
    """Delete a task."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks to delete.")
        return
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return
    updated_tasks = [t for t in tasks if t["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        print("⚠️ Task ID not found.")
        return
    # Re-index IDs
    for i, t in enumerate(updated_tasks, start=1):
        t["id"] = i
    save_tasks(updated_tasks)
    print(f"🗑️ Task {task_id} deleted.")


def main_menu():
    """Display menu and handle user input."""
    while True:
        print("\n==============================")
        print("🧾 TO-DO LIST MANAGER")
        print("==============================")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Mark task as done")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("👋 Goodbye! Your tasks are saved.")
            break
        else:
            print("⚠️ Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()
