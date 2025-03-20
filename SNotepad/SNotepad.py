import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox, QInputDialog, QAction, QMenu, QVBoxLayout, QWidget, QLabel, QSpinBox, QSlider, QPushButton
)
from PyQt5.QtGui import QFont, QTextCursor, QPalette, QColor
from PyQt5.QtCore import Qt

class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SNotepad")
        self.setGeometry(100, 100, 800, 600)

        # Настройки по умолчанию
        self.current_theme = "light"
        self.font_family = "Noto Sans"
        self.font_size = 12
        self.window_opacity = 1.0

        # Основное текстовое поле
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont(self.font_family, self.font_size))
        self.setCentralWidget(self.text_edit)

        # Применение начальной темы
        self.apply_theme()

        # Меню
        self.create_menu()

    def create_menu(self):
        # Меню "Файл"
        file_menu = self.menuBar().addMenu("Файл")

        new_action = QAction("Новый", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Открыть", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Сохранить как", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню "Правка"
        edit_menu = self.menuBar().addMenu("Правка")

        search_action = QAction("Поиск", self)
        search_action.triggered.connect(self.search_text)
        edit_menu.addAction(search_action)

        # Меню "Настройки"
        settings_menu = self.menuBar().addMenu("Настройки")

        theme_action = QAction("Сменить тему", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)

        settings_action = QAction("Открыть настройки", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        if not hasattr(self, "current_file") or not self.current_file:
            self.save_file_as()
        else:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.text_edit.toPlainText())
            QMessageBox.information(self, "Сохранение", "Файл успешно сохранен!")

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            self.current_file = file_path
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_edit.toPlainText())
            QMessageBox.information(self, "Сохранение", "Файл успешно сохранен!")

    def search_text(self):
        search_query, ok = QInputDialog.getText(self, "Поиск", "Введите текст для поиска:")
        if ok and search_query:
            cursor = self.text_edit.document().find(search_query)
            if not cursor.isNull():
                self.text_edit.setTextCursor(cursor)
                self.text_edit.setFocus()
            else:
                QMessageBox.information(self, "Поиск", "Текст не найден.")

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.apply_theme()

    def apply_theme(self):
        palette = QPalette()
        if self.current_theme == "dark":
            palette.setColor(QPalette.Window, QColor(49, 54, 59))  # Фон окна
            palette.setColor(QPalette.WindowText, QColor(239, 240, 241))  # Текст окна
            palette.setColor(QPalette.Base, QColor(35, 38, 41))  # Фон текстового поля
            palette.setColor(QPalette.Text, QColor(239, 240, 241))  # Текст
            palette.setColor(QPalette.Button, QColor(49, 54, 59))  # Кнопки
            palette.setColor(QPalette.ButtonText, QColor(239, 240, 241))  # Текст кнопок
        else:
            palette.setColor(QPalette.Window, QColor(239, 240, 241))  # Фон окна
            palette.setColor(QPalette.WindowText, QColor(35, 38, 41))  # Текст окна
            palette.setColor(QPalette.Base, QColor(255, 255, 255))  # Фон текстового поля
            palette.setColor(QPalette.Text, QColor(35, 38, 41))  # Текст
            palette.setColor(QPalette.Button, QColor(239, 240, 241))  # Кнопки
            palette.setColor(QPalette.ButtonText, QColor(35, 38, 41))  # Текст кнопок

        self.setPalette(palette)
        self.text_edit.setPalette(palette)

    def open_settings(self):
        settings_window = QWidget(self)
        settings_window.setWindowTitle("Настройки")
        settings_window.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        font_size_label = QLabel("Размер шрифта:", settings_window)
        layout.addWidget(font_size_label)

        font_size_spinbox = QSpinBox(settings_window)
        font_size_spinbox.setValue(self.font_size)
        layout.addWidget(font_size_spinbox)

        opacity_label = QLabel("Прозрачность окна:", settings_window)
        layout.addWidget(opacity_label)

        opacity_slider = QSlider(Qt.Horizontal, settings_window)
        opacity_slider.setMinimum(20)
        opacity_slider.setMaximum(100)
        opacity_slider.setValue(int(self.window_opacity * 100))
        layout.addWidget(opacity_slider)

        apply_button = QPushButton("Применить", settings_window)
        apply_button.clicked.connect(lambda: self.apply_settings(font_size_spinbox.value(), opacity_slider.value() / 100, settings_window))
        layout.addWidget(apply_button)

        settings_window.setLayout(layout)
        settings_window.show()

    def apply_settings(self, font_size, opacity, settings_window):
        self.font_size = font_size
        self.text_edit.setFont(QFont(self.font_family, self.font_size))
        self.window_opacity = opacity
        self.setWindowOpacity(self.window_opacity)
        settings_window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Breeze")  # Применение стиля Breeze
    window = NotepadApp()
    window.show()
    sys.exit(app.exec_())
