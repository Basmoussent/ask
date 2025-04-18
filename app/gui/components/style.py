from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette


class DarkPurpleStyle:
    """Classe pour définir le style sombre violet de l'application"""
    
    # Couleurs du thème
    DARK_BG = "#1E1E2E"
    DARK_SECONDARY = "#2D2D3F"
    PURPLE_ACCENT = "#9D4EDD"
    LIGHT_PURPLE = "#C77DFF"
    TEXT_COLOR = "#E0E0E0"
    HIGHLIGHT = "#B14EFF"
    BUTTON_HOVER = "#7B2CBF"
    
    @staticmethod
    def apply_to_app(app):
        """Applique le style à l'application entière"""
        app.setStyle("Fusion")
        
        # Palette de couleurs
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(DarkPurpleStyle.DARK_BG))
        palette.setColor(QPalette.WindowText, QColor(DarkPurpleStyle.TEXT_COLOR))
        palette.setColor(QPalette.Base, QColor(DarkPurpleStyle.DARK_SECONDARY))
        palette.setColor(QPalette.AlternateBase, QColor(DarkPurpleStyle.DARK_BG))
        palette.setColor(QPalette.ToolTipBase, QColor(DarkPurpleStyle.DARK_BG))
        palette.setColor(QPalette.ToolTipText, QColor(DarkPurpleStyle.TEXT_COLOR))
        palette.setColor(QPalette.Text, QColor(DarkPurpleStyle.TEXT_COLOR))
        palette.setColor(QPalette.Button, QColor(DarkPurpleStyle.DARK_SECONDARY))
        palette.setColor(QPalette.ButtonText, QColor(DarkPurpleStyle.TEXT_COLOR))
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(DarkPurpleStyle.LIGHT_PURPLE))
        palette.setColor(QPalette.Highlight, QColor(DarkPurpleStyle.PURPLE_ACCENT))
        palette.setColor(QPalette.HighlightedText, QColor(DarkPurpleStyle.TEXT_COLOR))
        
        app.setPalette(palette)
        
        # Style des widgets
        app.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial;
                font-size: 10pt;
                color: #E0E0E0;
            }
            QLineEdit {
                border: 1px solid #5A5A78;
                border-radius: 3px;
                padding: 5px;
                background-color: #2D2D3F;
                color: #E0E0E0;
            }
            QLineEdit:focus {
                border: 1px solid #9D4EDD;
            }
            QPushButton {
                background-color: #9D4EDD;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B2CBF;
            }
            QPushButton:pressed {
                background-color: #6622AA;
            }
            QPushButton:checked {
                background-color: #6622AA;
                border: 1px solid #C77DFF;
            }
            QComboBox {
                background-color: #2D2D3F;
                border: 1px solid #5A5A78;
                border-radius: 3px;
                padding: 5px;
                color: #E0E0E0;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #2D2D3F;
                border: 1px solid #5A5A78;
                color: #E0E0E0;
                selection-background-color: #9D4EDD;
            }
            QTableWidget {
                background-color: #2D2D3F;
                border: 1px solid #5A5A78;
                gridline-color: #3D3D5F;
                border-radius: 3px;
                color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #4A4A68;
                color: #E0E0E0;
                padding: 5px;
                border: 1px solid #3D3D5F;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #9D4EDD;
                color: white;
            }
            QTextEdit, QTextBrowser {
                background-color: #2D2D3F;
                border: 1px solid #5A5A78;
                border-radius: 3px;
                color: #E0E0E0;
                padding: 5px;
            }
            QSplitter::handle {
                background-color: #5A5A78;
            }
            QLabel {
                color: #C77DFF;
                font-weight: bold;
            }
        """)

