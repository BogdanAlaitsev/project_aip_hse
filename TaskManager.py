import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QDate

class TaskManager(QWidget):
    def __init__(self):
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
        # Поле ввода задачи
        self.task_input.setPlaceholderText("Введите задачу")
        self.layout.addWidget(self.task_input)

        # Приоритет
        self.priority_input.addItems(["Низкий", "Средний", "Высокий"])
        self.layout.addWidget(QLabel("Приоритет"))
        self.layout.addWidget(self.priority_input)

        # Дедлайн
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate())
        self.layout.addWidget(QLabel("Дедлайн"))
        self.layout.addWidget(self.deadline_input)

        # Кнопки
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

        # Список задач
        self.layout.addWidget(self.task_list)

        # Установка основного макета
        self.setLayout(self.layout)

    def add_task(self):
        task_name = self.task_input.text().strip()
        priority = self.priority_input.currentText()
        deadline = self.deadline_input.date().toString("yyyy-MM-dd")

        if task_name:
            task_info = {"task": task_name, "priority": priority, "deadline": deadline}
            self.task_list.addItem(f"{task_name} | Приоритет: {priority} | Дедлайн: {deadline}")
            self.task_input.clear()
            self.save_tasks()  # Сохраняем задачи после добавления
        else:
            QMessageBox.warning(self, "Ошибка", "Задача не может быть пустой.")

    def delete_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            self.task_list.takeItem(selected_task)
            self.save_tasks()  # Сохраняем задачи после удаления
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления.")

    def sort_by_priority(self):
        try:
            tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
            tasks.sort(key=lambda x: ["Низкий", "Средний", "Высокий"].index(x.split('|')[1].split(': ')[1].strip()))
            self.task_list.clear()
            self.task_list.addItems(tasks)
            self.save_tasks()  # Сохраняем задачи после сортировки
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка при сортировке: {str(e)}")

    def sort_by_deadline(self):
        try:
            tasks = [self.task_list.item(i).text() for i in range(self.task_list.count())]
            tasks.sort(key=lambda x: x.split('|')[-1].split(': ')[1].strip())
            self.task_list.clear()
            self.task_list.addItems(tasks)
            self.save_tasks()  # Сохраняем задачи после сортировки
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка при сортировке: {str(e)}")

    def save_tasks(self):
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
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                self.task_list.clear()
                for task in tasks:
                    task_info = f"{task['task']} | Приоритет: {task['priority']} | Дедлайн: {task['deadline']}"
                    self.task_list.addItem(task_info)

                QMessageBox.information(self, "Загрузка задач", "Задачи успешно загружены.")
                return tasks

        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл с задачами не найден.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка при загрузке задач: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
