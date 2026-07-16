# Assignment 01 - Command-Line Task Manager in Python

# Global list to store the tasks
tasks = []

def add_task(description):
    # Generate ID based on the last task added, or start at 1
    task_id = tasks[-1]["id"] + 1 if tasks else 1
    
    # Store task as a dictionary inside the list
    task = {
        "id": task_id,
        "description": description,
        "completed": False
    }
    tasks.append(task)
    print(f"Task '{description}' added with ID {task_id}.")

def view_tasks():
    # Check if we have any tasks to show
    if not tasks:
        print("No tasks available.")
        return
    
    # View all tasks in the list
    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        print(f"{task['id']}: {task['description']} [{status}]")

def mark_completed(task_id):
    # Search for task by ID and mark it as done
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            print(f"Task ID {task_id} marked as completed.")
            return
    print(f"No task found with ID {task_id}.")

def delete_task(task_id):
    global tasks
    # Rebuild the task list excluding the matching task ID
    tasks = [task for task in tasks if task["id"] != task_id]
    print(f"Task ID {task_id} deleted if it existed.")

def main(commands):
    # Loop over the automated test commands
    for command in commands:
        choice = command[0]
        
        if choice == "add":
            if len(command) > 1:
                desc = command[1]
                add_task(desc)
            else:
                print("Add command requires a description.")
                
        elif choice == "view":
            view_tasks()
            
        elif choice == "complete":
            if len(command) > 1:
                try:
                    task_id = int(command[1])
                    mark_completed(task_id)
                except ValueError:
                    print("Invalid task ID.")
            else:
                print("Complete command requires a task ID.")
                
        elif choice == "delete":
            if len(command) > 1:
                try:
                    task_id = int(command[1])
                    delete_task(task_id)
                except ValueError:
                    print("Invalid task ID.")
            else:
                print("Delete command requires a task ID.")
                
        elif choice == "exit":
            print("Exiting Task Manager. Goodbye!")
            break
            
        else:
            print(f"Invalid command: {choice}")

if __name__ == "__main__":
    # Example commands to test the application automatically as specified in the assignment
    commands_to_execute = [
        ("add", "Buy groceries"),
        ("add", "Walk the dog"),
        ("view",),
        ("complete", "1"),
        ("view",),
        ("delete", "2"),
        ("view",),
        ("exit",)
    ]
    main(commands_to_execute)
