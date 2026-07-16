Week 1 Assignments

This directory contains two python projects for Week 1.

Project Structure
- Assignment 01 - Command-Line Task Manager.py: A command-line program to add, view, complete, and delete tasks.
- Assignment 02 - Prompt-Driven Work Instructions.py: An AI assistant that generates manufacturing instructions for new car models using an LLM.
- readme.txt: Short report detailing the approach and folder info.


Assignment 01: Command-Line Task Manager

Approach
- Data Structure: The application uses a list filled with dictionaries. Each task dictionary stores the task ID, description, and status.
- Functions: The program is broken down into separate modular functions: add_task, view_tasks, mark_completed, and delete_task.
- Automated Input: We used a loop to run dummy commands automatically so the program runs without needing manual user inputs.

Challenges Faced: None

How to Run
Run the script using Python:
python "Assignment 01 - Command-Line Task Manager.py"


Assignment 02: Prompt-Driven Work Instructions Generator

Approach
- LLM Connection: Uses OpenAI client and prompt engineering to draft detailed, sequential assembly instructions.
- Environment variables: Loads OPENAI_API_KEY, OPENAI_API_BASEURL, and OPENAI_API_MODEL from the env file to make the api calls.
- Output: Prints the generated shop-floor instructions directly to the console.

Challenges Faced: None

How to Run
Run the script using Python:
python "Assignment 02 - Prompt-Driven Work Instructions.py"
