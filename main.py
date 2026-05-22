import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QMessageBox)

from PyQt6.QtCore import Qt
from control import Database

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список задач")
        self.resize(500, 300)
        self.db = Database()
        self.init_ui()
        self.load_table()

    def init_ui(self):
        laoyut = QVBoxLayout()
        form = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["№", "Задача", "Выполнено"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        laoyut.addWidget(self.table)

        self.line = QLineEdit()
        self.line.setPlaceholderText("Задача")
        form.addWidget(self.line)

        self.btn = QPushButton("Добавить")
        self.btn.clicked.connect(self.add)
        form.addWidget(self.btn)

        self.btn2 = QPushButton("Удалить")
        self.btn2.clicked.connect(self.delete)
        form.addWidget(self.btn2)

        laoyut.addLayout(form)
        self.setLayout(laoyut)

    def load_table(self, rows=None):
        if rows is None:
            rows = self.db.get_all()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate([row["id"], row["title"], row["is_done"]]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, j, item)

    def add(self):
        name = self.line.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите задачу!")
            return
        self.db.add(
            name, self.line.text().strip())
        
        self.load_table()

    def delete(self):
        tabl = self.table.currentRow()
        if tabl < 0:
            return
        
        title = self.table.item(tabl, 1).text()
        work_id = int(self.table.item(tabl, 0).text())
        
        
        self.db.delete(work_id)
        self.load_table()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()