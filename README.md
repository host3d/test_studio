# PriorityQueue Task Manager

A Python module to manage and execute tasks using a priority-based queue.
Each task is defined by a shell command and a priority level. The module ensures that tasks are executed in order of priority, with logging and state tracking for each task.



## Features

- Add tasks with priority levels ranging from 1 (lowest) to 10 (highest).
- Execute tasks in order of priority, starting with the highest.
- Track task states: `WAITING`, `SUCCESS`, or `ERROR`.
- View logs for task execution, including error logs and processing time.
- Automatically clear the queue after execution if needed.

---

## Requirements

This module uses standard Python libraries and requires no external dependencies. Ensure Python 3.7 or above is installed on your system.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/host3d/test_studio.git
   ```
2. Navigate to the project directory
   ```bash
   cd test_studio
   ```

## Usage

### 1. Add Tasks

Tasks are dictionaries containing two keys:

 - `command`: A shell command to execute.
 - `priority`: An integer priority (1-10).

Example
```python
tasks = [
    {"command": "ls", "priority": 5},
    {"command": "python --help", "priority": 10},
]
```

### 2. Initialize the Priority Queue

Create an instance of the PriorityQueue and add tasks:
```python
from priority_queue import PriorityQueue

queue = PriorityQueue()

# Add tasks to the queue
for task in tasks:
    queue.add_task(task)
```
### 3. Run Tasks
Execute all tasks in the queue:
```python
queue.run(auto_clear=True)
```

## Example Script

Here’s an example script to demonstrate the full functionality:
```python
from priority_queue import PriorityQueue

# Define tasks
tasks = [
    {"command": "ls", "priority": 5},
    {"command": "echo 'Hello, World!'", "priority": 1},
    {"command": "echo $HOME", "priority": 1},
    {"command": "python --help", "priority": 10},
]

# Initialize queue and add tasks
queue = PriorityQueue()
for task in tasks:
    queue.add_task(task)

# Process tasks
queue.run(auto_clear=True)
```

## Logging

The module logs task execution details:

 - Success or error states.
 - Execution time for each task.
 - Error logs for failed commands.
Logs are displayed in the console in the following format:
```
2024-12-16 12:00:00 - INFO - Starting task processing:
2024-12-16 12:00:01 - DEBUG - Task priority: 10, command: python --help
2024-12-16 12:00:02 - DEBUG -   SUCCESS, execute in: 1.23 sec
2024-12-16 12:00:02 - DEBUG - Task priority: 7, command: sfdf
2024-12-16 12:00:02 - DEBUG - 	ERROR, execute in: 0.06 sec
2024-12-16 12:00:02 - DEBUG - 	Log error: b"'sfdf' is not recognized as an internal or external command,\r\noperable program or batch file.\r\n"
2024-12-16 12:00:02 - INFO - 3 task(s) processed in 2.45 sec
```

## Limitations
 - Task priority must be between 1 and 10. Invalid priority levels are ignored.
 - Shell commands should be valid and executable in the current environment.

## Running Unit tests
This project includes unit tests to ensure the functionality of the PriorityQueue class. To run the tests:

1. Save the unit test code provided in the test_priority_queue.py file.
2. Make sure that the class PriorityQueue is in a file named priority_queue.py.
3. Run the tests using the following command:
```bash
python -m unittest test_priority_queue.py
```
## Unit Tests

The unit tests cover the following functionality:

### Adding tasks:

 - Valid tasks.
 - Tasks with invalid priorities.
 - Tasks with missing required keys (command and priority).

### Executing tasks:

 - Successful task execution (mocked via subprocess.check_output).
 - Task execution errors (mocked via subprocess.CalledProcessError).

### Queue management:
 - Clearing the queue with clear_queue().

### Running tasks:
 - Processing tasks with and without the auto_clear option.

### Order of Execution:
 - Verifying that tasks with the same priority are executed in the order they were added to the queue.