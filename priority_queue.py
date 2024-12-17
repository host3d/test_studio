"""
Module for managing and executing tasks with a priority queue.

This module provides a `PriorityQueue` class for handling tasks with priority levels,
executing them in order of priority, and managing their states. Each task consists of
a shell command to execute and a priority level.

Classes:
    PriorityQueue: Manages a priority-based task queue and executes tasks.

Constants:
    STATE_WAITING: Indicates a task is waiting to be executed.
    STATE_ERROR: Indicates a task encountered an error during execution.
    STATE_SUCCESS: Indicates a task executed successfully.

Usage:
    queue = PriorityQueue()

    tasks = [
        {"command": "dir", "priority": 5},
        {"command": "echo 'Up, Up, Down, Down, Left, Right, Left, Right, B, A'", "priority": 1},
        {"command": "python --help", "priority": 10},
        {"command": "dir", "priority": 1},
        {"command": "echo $HOME", "priority": 7},
        {"command": "echo 'HELLO Priority 0 !'", "priority": 0},
        {"command": "dir", "priority": 11},
    ]

    for task in tasks:
        queue.add_task(task)

    queue.run()
"""

from typing import Optional
from collections import defaultdict
import logging
import time
import subprocess

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constant
STATE_WAITING = 'WAITING'
STATE_ERROR = 'ERROR'
STATE_SUCCESS = 'SUCCESS'


class PriorityQueue:
    """ A class for managing tasks with priority levels."""
    def __init__(self, tasks: Optional[list] = None):
        """ Initializes the PriorityQueue.

        :param tasks: (Optional) A list of task dictionaries to initialize the queue. Defaults to None.
        """

        self._queue = defaultdict(list)
        self.log = logging.getLogger("PriorityQueue")

        for task in tasks or []:
            self.add_task(task)

    def add_task(self, task: dict) -> bool:
        """ Adds a task to the priority queue.

        :param task: A dictionary containing 'command' and 'priority' keys.
        :return: True if the task is successfully added, False otherwise.
        """

        try:
            if not 1 <= task['priority'] <= 10:
                self.log.error(f"Task priority must be between 0 and 10: {task['priority']}")
                return False
            data = {'command': task['command'], 'state': STATE_WAITING, 'log': None, 'time_processing': 0}
            self._queue[task["priority"]].append(data)
            self.log.debug(f"Add task priority: {task['priority']}, command: {data['command']}")
        except KeyError:
            self.log.error(f"Task need to have key 'priority' and 'command' not {task.keys()}")
            return False
        return True

    def _execute(self, priority: int, task_index: int) -> bool:
        """ Executes a task based on its priority and index in the queue.

        :param priority: The priority level of the task.
        :param task_index: The index of the task within its priority group.
        :return: True if the task executes successfully, False otherwise.
        """

        data = self._queue[priority][task_index]
        self.log.debug(f"Task priority: {priority}, command: {data['command']}")
        start = time.time()
        try:
            data['log'] = subprocess.check_output(data['command'], shell=True, stderr=subprocess.STDOUT)
            data['state'] = STATE_SUCCESS
        except subprocess.CalledProcessError as exception:
            data['log'] = exception.output
            data['state'] = STATE_ERROR

        data['time_processing'] = time.time() - start
        self.log.debug(f"\t{data['state']}, execute in: {data['time_processing']:.2f} sec")
        if data['state'] == STATE_ERROR:
            self.log.debug(f"\tLog error: {data['log']}")
            return False
        return True

    def clear_queue(self):
        """  Clears all tasks from the queue. """

        self.log.debug("Clear queue")
        self._queue = defaultdict(list)

    def run(self, auto_clear: Optional[bool] = False) -> bool:
        """  Executes all tasks in the queue, starting with the highest priority.

        :param auto_clear: (Optional) Clear the queue after execution. Defaults to False.
        :return: True if all tasks execute successfully else False.
        """
        self.log.info("Starting task processing:")
        start = time.time()
        _queue = self._queue.copy()
        result = []
        count = 0
        for priority, commands in sorted(_queue.items(), reverse=True):
            for index, command_data in enumerate(commands):
                if command_data['state'] == STATE_WAITING:
                    result.append(self._execute(priority, index))
                    count += 1

        self.log.info(f"{count} task(s) processed in {time.time() - start:.2f} sec")
        if auto_clear:
            self.clear_queue()

        return all(result)
