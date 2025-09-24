

TODO_FILE = "todo.txt"

def load_tasks():
    """Load tasks from file if it exists."""
    tasks = []
    try:
        with open(TODO_FILE, "r") as file:
            tasks = [line.strip() for line in file]
    except FileNotFoundError:
        pass  # No tasks yet
    return tasks

def save_tasks(tasks):
    """Save tasks to file."""
    with open(TODO_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def show_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("No tasks in your To-Do list.")
    else:
        print("\nYour To-Do List:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
    print("-" * 30)

def add_task(tasks):
    """Add a new task."""
    task = input("Enter task: ").strip()
    if task:
        tasks.append(task)
        print(f"Added: {task}")
    else:
        print("Cannot add empty task.")

def remove_task(tasks):
    """Remove a task by its number."""
    show_tasks(tasks)
    if tasks:
        try:
            num = int(input("Enter task number to remove: "))
            if 1 <= num <= len(tasks):
                removed = tasks.pop(num - 1)
                print(f"Removed: {removed}")
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    tasks = load_tasks()

    while True:
        print("\n=== To-Do List Menu ===")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Exit")

        choice = input("Your choice (1-4): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1-4.")

if __name__ == "__main__":
    main()
