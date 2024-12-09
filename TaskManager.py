"""
Task Manager Application
=========================
This application is a simple task manager built using PyQt6. 
It allows users to add, delete, sort, save, and load tasks.

Features:
---------
- Add tasks with priority and deadline.
- Delete selected tasks.
- Sort tasks by priority or deadline.
- Save tasks to a JSON file.
- Load tasks from a JSON file.

Usage:
------
Run this script to launch the application. 
The GUI will allow interaction with the task management features.

Author:
-------
Bogdan Alaitsev

"""

import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QDate


class TaskManager(QWidget):
    """
    TaskManager class provides a graphical interface for task management.

    Methods:
    --------
    __init__():
        Initializes the main window and components.

    init_ui():
        Sets up the layout and components of the application.

    add_task():
        Adds a new task to the list.

    delete_task():
        Deletes the selected task from the list.

    sort_by_priority():
        Sorts tasks in the list by priority.

    sort_by_deadline():
        Sorts tasks in the list by deadline.

    save_tasks():
        Saves the current tasks to a JSON file.

    load_tasks():
        Loads tasks from a JSON file into the list.
    """

    def __init__(self):
        """
        Initialize the Task Manager application.
        Sets up the main layout and loads existing tasks from file.
        """
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 400, 500)

        # Основные компоненты
        self.layout = QVBoxLayout()
        self.task_input = QLineEdit()
        self.priority_input = QComboBox()
        self.deadline_input = QDateEdit()
        self.task_list = QListWidget()

        self.init_ui()
        self.load_tasks()  # Загрузка задач при инициализации

    def init_ui(self):
        """
        Initializes the user interface components and layout.
        """
        self.task_input.setPlaceholderText("Введите задачу")
        self.layout.addWidget(self.task_input)

        self.priority_input.addItems(["Низкий", "Средний", "Высокий"])
        self.layout.addWidget(QLabel("Приоритет"))
        self.layout.addWidget(self.priority_input)

        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate())
        self.layout.addWidget(QLabel("Дедлайн"))
        self.layout.addWidget(self.deadline_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить задачу")
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        delete_button = QPushButton("Удалить задачу")
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        sort_priority_button = QPushButton("Сортировать по приоритету")
        sort_priority_button.clicked.connect(self.sort_by_priority)
        button_layout.addWidget(sort_priority_button)

        sort_deadline_button = QPushButton("Сортировать по дедлайну")
        sort_deadline_button.clicked.connect(self.sort_by_deadline)
        button_layout.addWidget(sort_deadline_button)

        save_button = QPushButton("Сохранить задачи")
        save_button.clicked.connect(self.save_tasks)
        button_layout.addWidget(save_button)

        load_button = QPushButton("Загрузить задачи")
        load_button.clicked.connect(self.load_tasks)
        button_layout.addWidget(load_button)

        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.task_list)
        self.setLayout(self.layout)

    def add_task(self):
        """
        Adds a new task to the task list based on user input.
        Saves tasks to the JSON file after addition.
        """
        task_name = self.task_input.text().strip()
        priority = self.priority_input.currentText()
        deadline = self.deadline_input.date().toString("yyyy-MM-dd")

        if task_name:
            task_info = {
                "task": task_name,
                "priority": priority,
                "deadline": deadline
            }
            self.task_list.addItem(
                f"{task_name} | Приоритет: {priority} | Дедлайн: {deadline}"
            )
            self.task_input.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Ошибка", "Задача не может быть пустой.")

    def delete_task(self):
        """
        Deletes the selected task from the task list.
        Saves tasks to the JSON file after deletion.
        """
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            self.task_list.takeItem(selected_task)
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления.")

    def sort_by_priority(self):
        """
        Sorts tasks in the list by priority in ascending order.
        Saves tasks to the JSON file after sorting.
        """
        try:
            tasks = [
                self.task_list.item(i).text()
                for i in range(self.task_list.count())
            ]
            tasks.sort(
                key=lambda x: ["Низкий", "Средний", "Высокий"].index(
                    x.split('|')[1].split(': ')[1].strip()
                )
            )
            self.task_list.clear()
            self.task_list.addItems(tasks)
            self.save_tasks()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def sort_by_deadline(self):
        """
        Sorts tasks in the list by deadline in ascending order.
        Saves tasks to the JSON file after sorting.
        """
        try:
            tasks = [
                self.task_list.item(i).text()
                for i in range(self.task_list.count())
            ]
            tasks.sort(key=lambda x: x.split('|')[-1].split(': ')[1].strip())
            self.task_list.clear()
            self.task_list.addItems(tasks)
            self.save_tasks()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def save_tasks(self):
        """
        Saves the current tasks to a JSON file (`tasks.json`) in the local directory.
        """
        tasks = []
        for i in range(self.task_list.count()):
            task_text = self.task_list.item(i).text()
            task_parts = task_text.split(" | ")
            task_info = {
                "task": task_parts[0],
                "priority": task_parts[1].split(": ")[1],
                "deadline": task_parts[2].split(": ")[1]
            }
            tasks.append(task_info)

        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        """
        Loads tasks from a JSON file (`tasks.json`) into the task list.
        Displays an error message if the file is not found or invalid.
        """
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                self.task_list.clear()
                for task in tasks:
                    task_info = (
                        f"{task['task']} | Приоритет: {task['priority']} | "
                        f"Дедлайн: {task['deadline']}"
                    )
                    self.task_list.addItem(task_info)

                QMessageBox.information(self, "Загрузка задач", "Задачи загружены.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл с задачами не найден.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")


def main():
    """
    Main function to launch the application.
    """
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
