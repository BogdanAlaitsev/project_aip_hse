import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDate
import os
import json
from TaskManager import TaskManager

class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        cls.window = TaskManager()

    def setUp(self):
        # Подготовка перед каждым тестом
        self.window.task_list.clear()
        if os.path.exists('tasks.json'):
            os.remove('tasks.json')

    def test_add_task(self):
        self.window.task_input.setText("Тестовая задача")
        self.window.priority_input.setCurrentText("Средний")
        self.window.deadline_input.setDate(QDate(2024, 12, 31))
        self.window.add_task()

        self.assertEqual(self.window.task_list.count(), 1)
        task_text = self.window.task_list.item(0).text()
        self.assertIn("Тестовая задача", task_text)
        self.assertIn("Средний", task_text)
        self.assertIn("2024-12-31", task_text)

    def test_delete_task(self):
        self.window.task_input.setText("Удаляемая задача")
        self.window.priority_input.setCurrentText("Низкий")
        self.window.deadline_input.setDate(QDate(2024, 12, 31))
        self.window.add_task()

        self.window.task_list.setCurrentRow(0)
        self.window.delete_task()

        self.assertEqual(self.window.task_list.count(), 0)

    def test_sort_by_priority(self):
        tasks = [
            {"task": "Task 1", "priority": "Высокий", "deadline": "2024-12-31"},
            {"task": "Task 2", "priority": "Низкий", "deadline": "2024-11-30"},
            {"task": "Task 3", "priority": "Средний", "deadline": "2024-10-31"}
        ]
        for task in tasks:
            self.window.task_list.addItem(f"{task['task']} | Приоритет: {task['priority']} | Дедлайн: {task['deadline']}")

        self.window.sort_by_priority()

        sorted_tasks = [self.window.task_list.item(i).text() for i in range(self.window.task_list.count())]
        self.assertIn("Task 2 | Приоритет: Низкий", sorted_tasks[0])
        self.assertIn("Task 3 | Приоритет: Средний", sorted_tasks[1])
        self.assertIn("Task 1 | Приоритет: Высокий", sorted_tasks[2])

    def test_sort_by_deadline(self):
        tasks = [
            {"task": "Task 1", "priority": "Высокий", "deadline": "2024-12-31"},
            {"task": "Task 2", "priority": "Низкий", "deadline": "2024-11-30"},
            {"task": "Task 3", "priority": "Средний", "deadline": "2024-10-31"}
        ]
        for task in tasks:
            self.window.task_list.addItem(f"{task['task']} | Приоритет: {task['priority']} | Дедлайн: {task['deadline']}")

        self.window.sort_by_deadline()

        sorted_tasks = [self.window.task_list.item(i).text() for i in range(self.window.task_list.count())]
        self.assertIn("Task 3 | Приоритет: Средний | Дедлайн: 2024-10-31", sorted_tasks[0])
        self.assertIn("Task 2 | Приоритет: Низкий | Дедлайн: 2024-11-30", sorted_tasks[1])
        self.assertIn("Task 1 | Приоритет: Высокий | Дедлайн: 2024-12-31", sorted_tasks[2])

    def test_save_and_load_tasks(self):
        self.window.task_input.setText("Сохраняемая задача")
        self.window.priority_input.setCurrentText("Высокий")
        self.window.deadline_input.setDate(QDate(2024, 12, 31))
        self.window.add_task()

        self.window.save_tasks()
        self.assertTrue(os.path.exists('tasks.json'))

        with open('tasks.json', 'r', encoding='utf-8') as f:
            tasks = json.load(f)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["task"], "Сохраняемая задача")
            self.assertEqual(tasks[0]["priority"], "Высокий")
            self.assertEqual(tasks[0]["deadline"], "2024-12-31")

        self.window.task_list.clear()
        self.window.load_tasks()
        self.assertEqual(self.window.task_list.count(), 1)

    @classmethod
    def tearDownClass(cls):
        cls.app.exit()


if __name__ == "__main__":
    unittest.main()
