import csv
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from InquirerPy import inquirer

console = Console()
TASKS_FILE = "tasks.csv"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    tasks = []
    with open(TASKS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tasks.append({
                "id": int(row["id"]),
                "description": row["description"],
                "done": row["done"].lower() == "true",
                "created_at": row["created_at"]
            })
    return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "description", "done", "created_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)


def add_task():
    description = inquirer.text(message="Enter task description:").execute().strip()
    if not description:
        console.print("[red]⚠️ Task cannot be empty[/red]")
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
    console.print(f"[green]✅ Task added:[/green] {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]📭 No tasks found.[/yellow]")
        return

    table = Table(title="📝 Your To-Do Tasks", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Description", justify="left")
    table.add_column("Status", justify="center")
    table.add_column("Created At", justify="center")

    for task in tasks:
        status = "[green]✅ Done[/green]" if task["done"] else "[red]❌ Pending[/red]"
        table.add_row(str(task["id"]), task["description"], status, task["created_at"])

    console.print(table)


def mark_done():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]No tasks to update.[/yellow]")
        return
    task_id = inquirer.number(message="Enter task ID to mark as done:").execute()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            console.print(f"[green]🎉 Task {task_id} marked as done![/green]")
            return
    console.print("[red]⚠️ Task ID not found.[/red]")


def delete_task():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]No tasks to delete.[/yellow]")
        return
    task_id = inquirer.number(message="Enter task ID to delete:").execute()
    updated_tasks = [t for t in tasks if t["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        console.print("[red]⚠️ Task ID not found.[/red]")
        return
    for i, t in enumerate(updated_tasks, start=1):
        t["id"] = i
    save_tasks(updated_tasks)
    console.print(f"[red]🗑️ Task {task_id} deleted.[/red]")


def main_menu():
    while True:
        console.print("\n[bold cyan]==============================[/bold cyan]")
        console.print("[bold magenta]🧾 TO-DO LIST MANAGER[/bold magenta]")
        console.print("[bold cyan]==============================[/bold cyan]")

        action = inquirer.select(
            message="Select an action:",
            choices=[
                "Add a new task",
                "View all tasks",
                "Mark task as done",
                "Delete a task",
                "Exit"
            ],
            default="View all tasks"
        ).execute()

        if action == "Add a new task":
            add_task()
        elif action == "View all tasks":
            list_tasks()
        elif action == "Mark task as done":
            mark_done()
        elif action == "Delete a task":
            delete_task()
        elif action == "Exit":
            console.print("[bold green]👋 Goodbye! Your tasks are saved to tasks.csv.[/bold green]")
            break


if __name__ == "__main__":
    main_menu()
