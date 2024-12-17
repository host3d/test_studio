import unittest
import subprocess

from unittest.mock import patch
from priority_queue import PriorityQueue
from priority_queue import STATE_SUCCESS
from priority_queue import STATE_ERROR


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        """Set up a fresh instance of PriorityQueue for each test."""
        self.queue = PriorityQueue()

    def test_add_task_valid(self):
        """Test adding a valid task to the queue."""
        task = {"command": "echo 'Hello, World!'", "priority": 5}
        self.assertTrue(self.queue.add_task(task))
        self.assertIn(task["priority"], self.queue._queue)
        self.assertEqual(len(self.queue._queue[task["priority"]]), 1)

    def test_add_task_invalid_priority(self):
        """Test adding a task with an invalid priority."""
        self.assertFalse(self.queue.add_task({"command": "echo 'Hello, World!'", "priority": 11}))

    def test_add_task_missing_keys(self):
        """Test adding a task missing required keys."""
        self.assertFalse(self.queue.add_task({"priority": 5}))

    @patch("subprocess.check_output")
    def test_execute_task_success(self, mock_check_output):
        """Test executing a task successfully."""
        mock_check_output.return_value = b"Task executed successfully"
        task = {"command": "echo 'Success!'", "priority": 3}
        self.queue.add_task(task)
        self.assertTrue(self.queue._execute(priority=task["priority"], task_index=0))
        task_data = self.queue._queue[task["priority"]][0]
        self.assertEqual(task_data["state"], STATE_SUCCESS)
        self.assertEqual(task_data["log"], b"Task executed successfully")

    @patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "cmd", b"Error occurred"))
    def test_execute_task_error(self, mock_check_output):
        """Test executing a task that results in an error."""
        task = {"command": "invalid_command", "priority": 3}
        self.queue.add_task(task)

        result = self.queue._execute(priority=task["priority"], task_index=0)
        self.assertFalse(result)
        task_data = self.queue._queue[task["priority"]][0]
        self.assertEqual(task_data["state"], STATE_ERROR)
        self.assertEqual(task_data["log"], b"Error occurred")

    def test_clear_queue(self):
        """Test clearing the queue."""
        task = {"command": "echo 'Hello, World!'", "priority": 5}
        self.queue.add_task(task)
        self.queue.clear_queue()
        self.assertEqual(len(self.queue._queue), 0)

    @patch("priority_queue.PriorityQueue._execute")
    def test_run_tasks(self, mock_execute):
        """Test running tasks in the queue."""
        mock_execute.return_value = True
        tasks = [
            {"command": "echo 'Task 1'", "priority": 3},
            {"command": "echo 'Task 2'", "priority": 5},
        ]
        for task in tasks:
            self.queue.add_task(task)

        self.assertTrue(self.queue.run(auto_clear=False))
        self.assertEqual(mock_execute.call_count, 2)

    @patch("priority_queue.PriorityQueue._execute")
    def test_run_tasks_with_auto_clear(self, mock_execute):
        """Test running tasks with the auto_clear option."""
        mock_execute.return_value = True
        tasks = [
            {"command": "echo 'Task 1'", "priority": 3},
            {"command": "echo 'Task 2'", "priority": 5},
        ]
        for task in tasks:
            self.queue.add_task(task)

        self.queue.run(auto_clear=True)
        self.assertEqual(len(self.queue._queue), 0)

    def test_add_two_tasks_same_priority(self):
        """Test that two tasks with the same priority are executed in the order they were added."""
        task_1 = {"command": "echo 'Task 1'", "priority": 5}
        task_2 = {"command": "echo 'Task 2'", "priority": 5}
        self.queue.add_task(task_1)
        self.queue.add_task({"command": "echo 'Task 10'", "priority": 10})
        self.queue.add_task(task_2)

        # Mock the _execute method to track execution order
        with patch.object(self.queue, "_execute") as mock_execute:
            mock_execute.side_effect = lambda priority, index: True

            # Run tasks
            self.queue.run(auto_clear=False)

            # Check the order of execution
            calls = [self.queue._queue[call[0][0]][call[0][1]]['command'] for call in mock_execute.call_args_list if call[0][0] == 5]  # Get task indexes
            self.assertEqual(calls, [task_1['command'], task_2['command']])  # Task 1 should run first, then Task 2

if __name__ == "__main__":
    unittest.main()
