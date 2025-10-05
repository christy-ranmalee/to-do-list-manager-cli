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
                "created_at": row["created_at"],
                "last_updated": row.get("last_updated", row["created_at"]),
            })
    return tasks


def save_tasks(tasks):
    fieldnames = ["id", "description", "done", "created_at", "last_updated"]
    tmp_file = f"{TASKS_FILE}.tmp"
    with open(tmp_file, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)
    os.replace(tmp_file, TASKS_FILE)


def generate_next_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def add_task():
    description = inquirer.text(message="Enter task description:").execute().strip()
    if not description:
        console.print("[red]⚠️ Task cannot be empty[/red]")
        return
    tasks = load_tasks()
    new_task = {
        "id": generate_next_id(tasks),
        "description": description,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(new_task)
    save_tasks(tasks)
    console.print(f"[green]✅ Task added:[/green] {description}")


def list_tasks(tasks=None):
    if tasks is None:
        tasks = load_tasks()
    if not tasks:
        console.print("[yellow]📭 No tasks found.[/yellow]")
        return

    table = Table(title="📝 Your To-Do Tasks", show_lines=True)
    table.add_column("ID", justify="center")
    table.add_column("Description", justify="left")
    table.add_column("Status", justify="center")
    table.add_column("Created At", justify="center")
    table.add_column("Last Updated", justify="center")

    for task in tasks:
        status = "[green]✅ Done[/green]" if task["done"] else "[red]❌ Pending[/red]"
        table.add_row(str(task["id"]), task["description"], status, task["created_at"], task["last_updated"])

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
            task["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            console.print(f"[green]🎉 Task {task_id} marked as done![/green]")
            return
    console.print("[red]⚠️ Task ID not found.[/red]")


def edit_task():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]No tasks to edit.[/yellow]")
        return
    task_id = inquirer.number(message="Enter task ID to edit:").execute()
    for task in tasks:
        if task["id"] == task_id:
            new_desc = inquirer.text(
                message="Enter new description:",
                default=task["description"]
            ).execute().strip()
            if not new_desc:
                console.print("[red]⚠️ Description cannot be empty.[/red]")
                return
            task["description"] = new_desc
            task["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            console.print(f"[cyan]✏️ Task {task_id} updated successfully![/cyan]")
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
    save_tasks(updated_tasks)
    console.print(f"[red]🗑️ Task {task_id} deleted.[/red]")


def filter_tasks():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    choice = inquirer.select(
        message="Filter tasks by:",
        choices=["Pending", "Completed", "All"]
    ).execute()
    if choice == "Pending":
        filtered = [t for t in tasks if not t["done"]]
    elif choice == "Completed":
        filtered = [t for t in tasks if t["done"]]
    else:
        filtered = tasks
    list_tasks(filtered)


def search_tasks():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    query = inquirer.text(message="Enter keyword to search:").execute().strip().lower()
    results = [t for t in tasks if query in t["description"].lower()]
    if results:
        console.print(f"[blue]🔍 Found {len(results)} matching tasks:[/blue]")
        list_tasks(results)
    else:
        console.print("[yellow]No matching tasks found.[/yellow]")


def clear_all_tasks():
    if not os.path.exists(TASKS_FILE):
        console.print("[yellow]No task file found.[/yellow]")
        return
    confirm = inquirer.confirm(message="Are you sure you want to delete ALL tasks?", default=False).execute()
    if confirm:
        os.remove(TASKS_FILE)
        console.print("[red]🧨 All tasks cleared![/red]")
    else:
        console.print("[cyan]Operation cancelled.[/cyan]")


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
                "Edit a task",
                "Search tasks",
                "Filter tasks",
                "Delete a task",
                "Clear all tasks",
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
        elif action == "Edit a task":
            edit_task()
        elif action == "Search tasks":
            search_tasks()
        elif action == "Filter tasks":
            filter_tasks()
        elif action == "Delete a task":
            delete_task()
        elif action == "Clear all tasks":
            clear_all_tasks()
        elif action == "Exit":
            console.print("[bold green]👋 Goodbye! Your tasks are saved to tasks.csv.[/bold green]")
            break


if __name__ == "__main__":
    main_menu()
