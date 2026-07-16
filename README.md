# Python Command-Line Task Manager (Assignment 01)

An elegant, modular, and robust command-line application developed in Python to manage daily tasks. This tool features task creation, category categorization, task priority definition, nice ASCII tabular layout visualization, and thorough input validation.

---

## 🛠️ Features & Enhancements

Key features and improvements implemented over the core requirements:
1. **Dynamic Task Scaling & Metadata**: Each task contains not only a description and completion status, but also:
   - **Priority**: Restricts input to High, Medium, Low (with automatic fallback handling for invalid types).
   - **Category**: Custom category grouping (e.g. Personal, Pets, Academic, Health, etc.).
2. **ASCII Grid View**: Built-in dynamic column scaling and alignment formatting for an clean visual representation of the active task database.
3. **Thorough Input Validation**:
   - Defensive checks for correct types (e.g., validating strings for description, integers for ID references).
   - Graceful fallback warnings if fields like `Priority` are misspelled (e.g., automatically falls back to `Medium`).
   - Clean, color-coded tag prefixes (`[ERROR]`, `[WARNING]`, `[SUCCESS]`, `[INFO]`) to track actions dynamically.
4. **Automated Command Execution**: Processes user scenarios using a simulated, predefined array of commands containing arguments, preserving automated testability without prompting.

---

## 📂 Project Structure

```text
AI_AE_Assignments/
├── task_manager.py     # Main Python script containing business logic and task database
└── README.md           # Documentation, design decisions, and system walkthrough
```

---

## 🚀 Execution & Verification

To run this command-line manager, execute the script with your local Python 3 environment:

```powershell
python task_manager.py
```

### Script Execution Log Output Screenshot Preview

```text
======================================================================
                COMMAND-LINE TASK MANAGER INITIALIZED               
======================================================================

⚡ Command #1: Action 'add' with args ('Buy groceries', 'High', 'Personal')
[SUCCESS] Task 'Buy groceries' added with ID 1 (Priority: High, Category: Personal).

⚡ Command #2: Action 'add' with args ('Walk the dog', 'Medium', 'Pets')
[SUCCESS] Task 'Walk the dog' added with ID 2 (Priority: Medium, Category: Pets).

⚡ Command #3: Action 'add' with args ('Prepare assignment report', 'High', 'Academic')
[SUCCESS] Task 'Prepare assignment report' added with ID 3 (Priority: High, Category: Academic).

⚡ Command #4: Action 'add' with args ('Read Python article',)
[SUCCESS] Task 'Read Python article' added with ID 4 (Priority: Medium, Category: General).

⚡ Command #5: Action 'add' with args ('Drink water', 'SuperHigh', 'Health')
[WARNING] Invalid priority 'Superhigh'. Defaulting to 'Medium'.
[SUCCESS] Task 'Drink water' added with ID 5 (Priority: Medium, Category: Health).

⚡ Command #6: Action 'view' with args ()

+------+--------------------------------+------------+--------------+------------+
| ID   | Task Description               | Priority   | Category     | Status     |
+------+--------------------------------+------------+--------------+------------+
|    1 | Buy groceries                  | High       | Personal     | Pending    |
|    2 | Walk the dog                   | Medium     | Pets         | Pending    |
|    3 | Prepare assignment report      | High       | Academic     | Pending    |
|    4 | Read Python article            | Medium     | General      | Pending    |
|    5 | Drink water                    | Medium     | Health       | Pending    |
+------+--------------------------------+------------+--------------+------------+


⚡ Command #7: Action 'complete' with args ('1',)
[SUCCESS] Task ID 1 marked as completed.

⚡ Command #8: Action 'view' with args ()

+------+--------------------------------+------------+--------------+------------+
| ID   | Task Description               | Priority   | Category     | Status     |
+------+--------------------------------+------------+--------------+------------+
|    1 | Buy groceries                  | High       | Personal     | Completed  |
|    2 | Walk the dog                   | Medium     | Pets         | Pending    |
|    3 | Prepare assignment report      | High       | Academic     | Pending    |
|    4 | Read Python article            | Medium     | General      | Pending    |
|    5 | Drink water                    | Medium     | Health       | Pending    |
+------+--------------------------------+------------+--------------+------------+


⚡ Command #9: Action 'complete' with args ('99',)
[ERROR] Task ID 99 not found.

⚡ Command #10: Action 'complete' with args ('invalid_id',)
[ERROR] Invalid task ID 'invalid_id'. Task ID must be an integer.

⚡ Command #11: Action 'delete' with args ('2',)
[SUCCESS] Task ID 2 deleted successfully.

⚡ Command #12: Action 'view' with args ()

+------+--------------------------------+------------+--------------+------------+
| ID   | Task Description               | Priority   | Category     | Status     |
+------+--------------------------------+------------+--------------+------------+
|    1 | Buy groceries                  | High       | Personal     | Completed  |
|    3 | Prepare assignment report      | High       | Academic     | Pending    |
|    4 | Read Python article            | Medium     | General      | Pending    |
|    5 | Drink water                    | Medium     | Health       | Pending    |
+------+--------------------------------+------------+--------------+------------+


⚡ Command #13: Action 'delete' with args ('99',)
[ERROR] Task ID 99 not found. Deletion failed.

⚡ Command #14: Action 'delete' with args ('wrong_id',)
[ERROR] Invalid task ID 'wrong_id'. Task ID must be an integer.

⚡ Command #15: Action 'exit' with args ()

Exiting Task Manager. Goodbye!

======================================================================
                COMMAND-LINE TASK MANAGER SHUTDOWN
======================================================================
```

---

## 🧠 Approach & Key Decisions

- **In-Memory Storage**: An in-memory Python `list` containing dynamic dictionaries (`{"id": task_id, "description": desc, "completed": False, "priority": prio, "category": cat}`) was chosen. This allows efficient $O(1)$ operations for appends and $O(N)$ for retrieval/deletions, keeping the system clean and performant.
- **Backwards Compatibility**: Structured command-parsing dynamically inspects tuple length (`len(command)`), allowing the system to consume standard command lists as well as multi-argument commands (e.g. including custom category/priorities) seamlessly.
- **Safety First**: Implemented exception blocks for converting CLI IDs (`int(val)`) to capture strings or floating-point decimals, preventing program crashing during parsing errors.

---

## ⚠️ Challenges & Resolutions

- **Challenge**: The programmatic interface restricts terminal user inputs (i.e. `input()` commands) to obey automated validation testing.
  - **Resolution**: Designed the system around a flexible command driver loop processing an array of instruction tuples. This maps perfectly to the requested automation framework while retaining the behavior of modular functions.
- **Challenge**: Scaling visual layouts when task descriptions are too long, causing borders to wrap and corrupt lines.
  - **Resolution**: Intercepted string width evaluation during representation formatting. Any description exceeding 30 characters is appended with a trailing ellipsis (`...`), keeping visual grids beautifully aligned.
