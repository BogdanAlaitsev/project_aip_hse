import unittest
import json
import os
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication
from TaskManager import TaskManager


class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Создаем приложение для тестов

    def setUp(self):
        self.manager = TaskManager()  # Создаем экземпляр TaskManager перед каждым тестом

    def tearDown(self):
        # Удаляем временный файл задач после каждого теста
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")

    def test_add_task_valid(self):
        # Положительный случай добавления задачи
        self.manager.task_input.setText("Сделать домашнее задание")
        self.manager.priority_input.setCurrentText("Высокий")
        self.manager.deadline_input.setDate(QDate(2024, 12, 31))
        self.manager.add_task()

        self.assertEqual(self.manager.task_list.count(), 1)
        self.assertIn("Сделать домашнее задание | Приоритет: Высокий | Дедлайн: 2024-12-31",
                      self.manager.task_list.item(0).text())

    def test_add_task_invalid(self):
        # Отрицательный случай добавления пустой задачи
        self.manager.task_input.setText("")  # Пустой ввод
        self.manager.add_task()

        self.assertEqual(self.manager.task_list.count(), 0)

    def test_delete_task(self):
        # Положительный случай удаления задачи
        self.manager.task_input.setText("Сделать домашнее задание")
        self.manager.add_task()
        self.manager.task_list.setCurrentRow(0)
        self.manager.delete_task()

        self.assertEqual(self.manager.task_list.count(), 0)

        # Отрицательный случай удаления без выбора задачи
        self.manager.delete_task()  # Ничего не выбрано
        self.assertEqual(self.manager.task_list.count(), 0)

    def test_sort_by_priority(self):
        # Добавление задач с разным приоритетом
        self.manager.task_input.setText("Задача 1")
        self.manager.priority_input.setCurrentText("Низкий")
        self.manager.add_task()

        self.manager.task_input.setText("Задача 2")
        self.manager.priority_input.setCurrentText("Средний")
        self.manager.add_task()

        self.manager.task_input.setText("Задача 3")
        self.manager.priority_input.setCurrentText("Высокий")
        self.manager.add_task()

        # Проверка сортировки по приоритету
        self.manager.sort_by_priority()
        sorted_tasks = [self.manager.task_list.item(i).text() for i in range(self.manager.task_list.count())]
        self.assertIn("Задача 1", sorted_tasks[0])
        self.assertIn("Задача 2", sorted_tasks[1])
        self.assertIn("Задача 3", sorted_tasks[2])

    def test_sort_by_deadline(self):
        # Добавление задач с разными дедлайнами
        self.manager.task_input.setText("Задача 1")
        self.manager.deadline_input.setDate(QDate(2024, 12, 31))
        self.manager.add_task()

        self.manager.task_input.setText("Задача 2")
        self.manager.deadline_input.setDate(QDate(2024, 1, 1))
        self.manager.add_task()

        self.manager.task_input.setText("Задача 3")
        self.manager.deadline_input.setDate(QDate(2024, 6, 15))
        self.manager.add_task()

        # Проверка сортировки по дедлайну
        self.manager.sort_by_deadline()
        sorted_tasks = [self.manager.task_list.item(i).text() for i in range(self.manager.task_list.count())]
        self.assertIn("Задача 2", sorted_tasks[0])
        self.assertIn("Задача 3", sorted_tasks[1])
        self.assertIn("Задача 1", sorted_tasks[2])

    def test_save_and_load_tasks(self):
        # Добавление и сохранение задач
        self.manager.task_input.setText("Задача 1")
        self.manager.add_task()

        self.manager.task_input.setText("Задача 2")
        self.manager.add_task()

        self.manager.save_tasks()
        self.assertTrue(os.path.exists("tasks.json"))

        # Загрузка задач из файла
        self.manager.task_list.clear()
        self.manager.load_tasks()
        self.assertEqual(self.manager.task_list.count(), 2)

    @classmethod
    def tearDownClass(cls):
        del cls.app  # Завершаем приложение после всех тестов


if __name__ == "__main__":
    unittest.main()
