"""
Assignment 01 - Command-Line Task Manager
Author: vusky102 (Google DeepMind Antigravity)
Date: July 16, 2026

Description:
A modular Python-based CLI Task Manager utilizing automated commands.
Implements task creation, viewing, completion status, deletion, validation,
and decorative alignment.
"""

# Global in-memory task database
tasks = []

def add_task(description, priority="Medium", category="General"):
    """
    Adds a new task to the task list with validation and auto-incrementing ID.
    """
    # Defensive programming: validate input types
    if not isinstance(description, str) or not description.strip():
        print("[ERROR] Task description cannot be empty.")
        return False
    
    # Clean inputs
    description = description.strip()
    priority = priority.strip().capitalize()
    category = category.strip().capitalize()

    # Validate Priority options
    valid_priorities = {"Low", "Medium", "High"}
    if priority not in valid_priorities:
        print(f"[WARNING] Invalid priority '{priority}'. Defaulting to 'Medium'.")
        priority = "Medium"

    # Auto-incrementing ID selection
    task_id = tasks[-1]["id"] + 1 if tasks else 1

    task = {
        "id": task_id,
        "description": description,
        "completed": False,
        "priority": priority,
        "category": category
    }
    tasks.append(task)
    print(f"[SUCCESS] Task '{description}' added with ID {task_id} (Priority: {priority}, Category: {category}).")
    return True

def view_tasks():
    """
    Displays all tasks in a beautifully formatted ANSI console table.
    """
    if not tasks:
        print("\n+-------------------------------------------------------------+")
        print("|                  No tasks available yet!                    |")
        print("+-------------------------------------------------------------+\n")
        return

    # Table formatting definitions
    col_widths = {
        "id": 4,
        "desc": 30,
        "priority": 10,
        "category": 12,
        "status": 10
    }
    
    # Print Table Header
    header_separator = (
        f"+{'-' * (col_widths['id'] + 2)}"
        f"+{'-' * (col_widths['desc'] + 2)}"
        f"+{'-' * (col_widths['priority'] + 2)}"
        f"+{'-' * (col_widths['category'] + 2)}"
        f"+{'-' * (col_widths['status'] + 2)}"
        f"+"
    )
    
    print("\n" + header_separator)
    print(
        f"| {'ID'.ljust(col_widths['id'])} "
        f"| {'Task Description'.ljust(col_widths['desc'])} "
        f"| {'Priority'.ljust(col_widths['priority'])} "
        f"| {'Category'.ljust(col_widths['category'])} "
        f"| {'Status'.ljust(col_widths['status'])} |"
    )
    print(header_separator)
    
    # Print Table Rows
    for task in tasks:
        status_str = "Completed" if task["completed"] else "Pending"
        
        # Clip long task descriptions to fit layout beautifully
        desc_clipped = task["description"]
        if len(desc_clipped) > col_widths["desc"]:
            desc_clipped = desc_clipped[:col_widths["desc"] - 3] + "..."

        print(
            f"| {str(task['id']).rjust(col_widths['id'])} "
            f"| {desc_clipped.ljust(col_widths['desc'])} "
            f"| {task['priority'].ljust(col_widths['priority'])} "
            f"| {task['category'].ljust(col_widths['category'])} "
            f"| {status_str.ljust(col_widths['status'])} |"
        )
    print(header_separator + "\n")

def mark_completed(task_id):
    """
    Marks a task with the given ID as completed with handling for invalid IDs.
    """
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"[INFO] Task ID {task_id} is already marked as completed.")
                return True
            task["completed"] = True
            print(f"[SUCCESS] Task ID {task_id} marked as completed.")
            return True
    
    print(f"[ERROR] Task ID {task_id} not found.")
    return False

def delete_task(task_id):
    """
    Deletes a task with the given ID from the list.
    """
    global tasks
    initial_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(tasks) < initial_length:
        print(f"[SUCCESS] Task ID {task_id} deleted successfully.")
        return True
    else:
        print(f"[ERROR] Task ID {task_id} not found. Deletion failed.")
        return False

def main(commands):
    """
    Processes a list of commands sequentially to simulate run-time inputs.
    Supported command structures:
    - ('add', description, priority, category) - priority and category are optional
    - ('view',)
    - ('complete', task_id)
    - ('delete', task_id)
    - ('exit',)
    """
    print("=" * 70)
    print("                COMMAND-LINE TASK MANAGER INITIALIZED               ")
    print("=" * 70)

    for cmd_idx, command in enumerate(commands, start=1):
        if not command:
            continue
        
        choice = command[0].strip().lower()
        print(f"\n⚡ Command #{cmd_idx}: Action '{choice}' with args {command[1:]}")
        
        if choice == "add":
            if len(command) > 1:
                description = command[1]
                priority = command[2] if len(command) > 2 else "Medium"
                category = command[3] if len(command) > 3 else "General"
                add_task(description, priority, category)
            else:
                print("[ERROR] Add command requires at least a task description.")
        
        elif choice == "view":
            view_tasks()
            
        elif choice == "complete":
            if len(command) > 1:
                try:
                    task_id = int(command[1])
                    mark_completed(task_id)
                except ValueError:
                    print(f"[ERROR] Invalid task ID '{command[1]}'. Task ID must be an integer.")
            else:
                print("[ERROR] Complete command requires a task ID.")
                
        elif choice == "delete":
            if len(command) > 1:
                try:
                    task_id = int(command[1])
                    delete_task(task_id)
                except ValueError:
                    print(f"[ERROR] Invalid task ID '{command[1]}'. Task ID must be an integer.")
            else:
                print("[ERROR] Delete command requires a task ID.")
                
        elif choice == "exit":
            print("\nExiting Task Manager. Goodbye!")
            break
            
        else:
            print(f"[ERROR] Unknown command action: '{choice}'")

    print("\n" + "=" * 70)
    print("                COMMAND-LINE TASK MANAGER SHUTDOWN                  ")
    print("=" * 70)

if __name__ == "__main__":
    # Test suite with typical scenarios, edge cases, and invalid inputs to verify robustness.
    commands_to_execute = [
        # Adding normal tasks
        ("add", "Buy groceries", "High", "Personal"),
        ("add", "Walk the dog", "Medium", "Pets"),
        ("add", "Prepare assignment report", "High", "Academic"),
        # Adding task with minimum arguments (defaulting category/priority)
        ("add", "Read Python article"),
        # Adding with invalid priority (should fallback to Medium)
        ("add", "Drink water", "SuperHigh", "Health"),
        # View command
        ("view",),
        # Complete task ID 1
        ("complete", "1"),
        # View change
        ("view",),
        # Handle invalid ID for completion
        ("complete", "99"),
        ("complete", "invalid_id"),
        # Delete task ID 2
        ("delete", "2"),
        # View change
        ("view",),
        # Handle invalid ID for deletion
        ("delete", "99"),
        ("delete", "wrong_id"),
        # Final exit
        ("exit",)
    ]
    main(commands_to_execute)
