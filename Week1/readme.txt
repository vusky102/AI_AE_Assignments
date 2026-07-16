Assignment 01 - Command-Line Task Manager

A command-line task manager application written in Python. This program allows users to add tasks, view tasks, mark tasks as completed, and delete tasks from their list.

Project Structure
- Assignment 01 - Command-Line Task Manager.py: The main Python script.
- readme.txt: Short report explaining the approach and challenges.

Approach
- Data Structure: The application uses a list filled with dictionaries. Each task dictionary stores the task ID, description, and status.
- Functions: The program is broken down into separate modular functions: add_task, view_tasks, mark_completed, and delete_task.
- Automated Input: We used a loop to run dummy commands automatically so the program runs without needing manual user inputs.

Challenges Faced
- Incrementing IDs: When tasks are deleted, the next task ID must still increment correctly. We resolved this by getting the ID of the last element in the list and adding 1.
- Input Validation: Handling cases to prevent errors if the user passes an invalid non-integer string as a task ID. We added a try-except block to catch parsing errors.

How to Run
Run the script using Python:
python "Assignment 01 - Command-Line Task Manager.py"
