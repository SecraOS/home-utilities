import sys
from decimal import Decimal, InvalidOperation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QStackedWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Калькулятор')
        self.setGeometry(100, 100, 300, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
            }
            QLineEdit {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 2px solid #5E81AC;
                border-radius: 10px;
                padding: 10px;
                font-size: 24px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: 2px solid #81A1C1;
                border-radius: 15px;
                padding: 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #4C566A;
            }
        """)

        self.layout = QVBoxLayout()

        # Поле для ввода и вывода
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.display.setFont(QFont('Arial', 20))
        self.layout.addWidget(self.display)

        # Верхняя панель с кнопками управления
        control_layout = QHBoxLayout()

        # Добавляем растягивающийся элемент слева
        control_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Кнопки управления (C, ←)
        for button_text in ['C', '←']:
            button = QPushButton(button_text, self)
            button.setFixedSize(70, 70)
            if button_text == 'C':
                button.clicked.connect(self.clear_display)
            elif button_text == '←':
                button.clicked.connect(self.backspace)
            control_layout.addWidget(button)

        self.layout.addLayout(control_layout)

        # Создаем стек для переключения между страницами кнопок
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Основная страница с цифрами и операциями
        self.main_buttons = self.create_button_page([
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ])
        self.stacked_widget.addWidget(self.main_buttons)

        # Страница со скобками
        self.bracket_buttons = self.create_bracket_page()
        self.stacked_widget.addWidget(self.bracket_buttons)

        self.setLayout(self.layout)

    def create_button_page(self, buttons_layout):
        page = QWidget()
        layout = QVBoxLayout()

        for row in buttons_layout:
            h_layout = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text, self)
                button.setFixedSize(70, 70)
                if button_text == '()':
                    button.clicked.connect(self.toggle_pages)
                elif button_text == '=':
                    button.clicked.connect(self.calculate_result)
                else:
                    button.clicked.connect(self.on_button_click)
                h_layout.addWidget(button)
            layout.addLayout(h_layout)

        page.setLayout(layout)
        return page

    def create_bracket_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Добавляем растягивающийся элемент сверху
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки скобок
        h_layout = QHBoxLayout()
        # Добавляем растягивающийся элемент слева
        h_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        for button_text in ['(', ')', '()']:
            button = QPushButton(button_text, self)
            button.setFixedSize(70, 70)
            if button_text == '()':
                button.clicked.connect(self.toggle_pages)
            else:
                button.clicked.connect(self.on_button_click)
            h_layout.addWidget(button)
        layout.addLayout(h_layout)

        page.setLayout(layout)
        return page

    def toggle_pages(self):
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def on_button_click(self):
        button = self.sender()
        text = button.text()
        self.display.setText(self.display.text() + text)

    def clear_display(self):
        self.display.clear()

    def backspace(self):
        current_text = self.display.text()
        self.display.setText(current_text[:-1])

    def calculate_result(self):
        try:
            # Используем Decimal для точных вычислений
            expression = self.display.text()
            result = str(eval(expression, {"__builtins__": None}, {"Decimal": Decimal}))
            self.display.setText(result)
        except (InvalidOperation, SyntaxError, NameError):
            self.display.setText("Ошибка")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
