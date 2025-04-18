from app.core.bloc.base_bloc import BaseBloc
from PySide6.QtWidgets import (
	QVBoxLayout, QHBoxLayout,
	QLineEdit, QPushButton, QLabel, QTextEdit
)

class ParseBlock(BaseBloc):
    """Bloc pour parser une valeur à partir d'une réponse"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Extraction de valeur"
        self.title_label.setText(self.title)
        self.previous_response = None
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        
    def init_ui(self):
        super().init_ui()
        
        # Layout des délimiteurs
        self.delimiters_layout = QVBoxLayout()
        
        # Délimiteur gauche
        self.left_delim_layout = QHBoxLayout()
        self.left_delim_label = QLabel("Délimiteur gauche:")
        self.left_delim_input = QLineEdit()
        
        self.left_delim_layout.addWidget(self.left_delim_label)
        self.left_delim_layout.addWidget(self.left_delim_input)
        
        # Délimiteur droit
        self.right_delim_layout = QHBoxLayout()
        self.right_delim_label = QLabel("Délimiteur droit:")
        self.right_delim_input = QLineEdit()
        
        self.right_delim_layout.addWidget(self.right_delim_label)
        self.right_delim_layout.addWidget(self.right_delim_input)
        
        # Index d'occurrence
        self.occurrence_layout = QHBoxLayout()
        self.occurrence_label = QLabel("Index d'occurrence:")
        self.occurrence_input = QLineEdit("0")
        self.occurrence_input.setToolTip("0 pour la première occurrence, 1 pour la deuxième, etc.")
        
        self.occurrence_layout.addWidget(self.occurrence_label)
        self.occurrence_layout.addWidget(self.occurrence_input)
        
        # Aperçu de la valeur trouvée
        self.preview_layout = QVBoxLayout()
        self.preview_label = QLabel("Aperçu de la valeur extraite:")
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(100)
        
        self.preview_layout.addWidget(self.preview_label)
        self.preview_layout.addWidget(self.preview_text)
        
        # Bouton d'extraction
        self.extract_button = QPushButton("Extraire")
        self.extract_button.clicked.connect(self.execute)
        
        # Ajouter les layouts au layout du contenu
        self.content_layout.addLayout(self.delimiters_layout)
        self.content_layout.addLayout(self.left_delim_layout)
        self.content_layout.addLayout(self.right_delim_layout)
        self.content_layout.addLayout(self.occurrence_layout)
        self.content_layout.addLayout(self.preview_layout)
        self.content_layout.addWidget(self.extract_button)
        
    def set_previous_response(self, response):
        """Définit la réponse précédente à utiliser pour l'extraction"""
        self.previous_response = response
        
    def get_result(self):
        """Retourne la valeur extraite"""
        return self.preview_text.toPlainText()
        
    def execute(self):
        """Extrait la valeur selon les délimiteurs définis"""
        if not self.previous_response:
            self.preview_text.setText("Aucune réponse précédente disponible")
            return None
            
        left_delim = self.left_delim_input.text()
        right_delim = self.right_delim_input.text()
        
        try:
            occurrence = int(self.occurrence_input.text())
        except ValueError:
            occurrence = 0
            
        if not left_delim and not right_delim:
            self.preview_text.setText("Spécifiez au moins un délimiteur")
            return None
            
        try:
            text = self.previous_response
            
            if left_delim:
                parts = text.split(left_delim)
                if len(parts) <= occurrence + 1:
                    self.preview_text.setText("Délimiteur gauche non trouvé ou occurrence trop élevée")
                    return None
                text = parts[occurrence + 1]
                
            if right_delim:
                parts = text.split(right_delim)
                if len(parts) < 1:
                    self.preview_text.setText("Délimiteur droit non trouvé")
                    return None
                text = parts[0]
                
            self.preview_text.setText(text)
            return text
            
        except Exception as e:
            self.preview_text.setText(f"Erreur lors de l'extraction: {str(e)}")
            return None