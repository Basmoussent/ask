from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout,
	QPushButton, QLabel
)
from PySide6.QtGui import QFont

class BaseBloc(QWidget):
    """Classe de base pour les blocs dans le stack"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Bloc"
        self.collapsed = False
        self.init_ui()
        
    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header with title and collapse button
        self.header = QWidget()
        self.header.setStyleSheet("background-color: #6e4491;")
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(10, 5, 10, 5)
        
        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.collapse_button = QPushButton("-")
        self.collapse_button.setFixedSize(30, 30)
        self.collapse_button.clicked.connect(self.toggle_collapse)
        
        
        self.delete_button = QPushButton("×")
        self.delete_button.setFixedSize(30, 30)

        self.collapse_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #22043b;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3c0560;
            }
        """)

        self.delete_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #b00020;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.collapse_button)
        self.header_layout.addWidget(self.delete_button)
        
        # Content container
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add widgets to main layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.content)

    def toggle_collapse(self):
        self.collapsed = not self.collapsed
        self.content.setVisible(not self.collapsed)
        self.collapse_button.setText("+" if self.collapsed else "-")
       
        
    def get_result(self):
        """Doit être implémenté par les classes dérivées"""
        raise NotImplementedError("Les sous-classes doivent implémenter get_result()")
        
    def execute(self):
        """Exécute le bloc et retourne son résultat"""
        raise NotImplementedError("Les sous-classes doivent implémenter execute()")