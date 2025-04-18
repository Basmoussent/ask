import sys
from PySide6.QtWidgets import QApplication

from app.gui.components.style import DarkPurpleStyle
from app.core.workspace_manager import RequestWorkspace

# Lancer l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Appliquer le style sombre violet
    DarkPurpleStyle.apply_to_app(app)
    
    window = RequestWorkspace()
    window.show()
    sys.exit(app.exec())