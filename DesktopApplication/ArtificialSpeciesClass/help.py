from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QGridLayout, QLabel, QComboBox, QSlider, QMessageBox, QMenu)
class Help:
    def __init__(self):
        pass

    def show_help(self):
        help_text = """
        This is a help message

        This is a help message
        
        This is a help message

        """
        QMessageBox.information(self, "Help", help_text)