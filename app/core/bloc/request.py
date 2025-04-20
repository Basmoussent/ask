from app.core.bloc.base_bloc import BaseBloc
from app.core.request_engine import Request as RequestEngine
from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
	QPushButton, QComboBox, QTableWidget, QTextEdit, QLabel,
	QHeaderView, QStackedWidget, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class RequestBlock(BaseBloc):
    """Bloc pour éditer et envoyer une requête HTTP"""
    def __init__(self, parent=None):
        self.request = RequestEngine()  # Utiliser RequestEngine au lieu de Request
        super().__init__(parent)
        self.title = "Requête HTTP"
        self.title_label.setText(self.title)
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
        
        # URL et méthode
        self.url_layout = QHBoxLayout()
        
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
        self.method_combo.setFixedWidth(100)

        self.url_input = QLineEdit()
        self.url_input.setText("https://google.com")

        
        method_label = QLabel("Méthode:")
        method_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.url_layout.addWidget(method_label)
        self.url_layout.addWidget(self.method_combo)
        self.url_layout.addWidget(self.url_input)
        
        # Onglets pour les paramètres, headers, cookies, etc.
        self.tabs = QTabWidget()
        
        # Tab pour les paramètres
        self.params_tab = QWidget()
        self.params_layout = QVBoxLayout(self.params_tab)
        
        self.param_header = QHBoxLayout()
        self.param_title = QLabel("Paramètres")
        self.add_param_button = QPushButton("+")
        self.add_param_button.setFixedSize(24, 24)
        self.add_param_button.clicked.connect(self.add_parameter_row)
        
        self.param_header.addWidget(self.param_title)
        self.param_header.addStretch()
        self.param_header.addWidget(self.add_param_button)
        
        self.params_layout.addLayout(self.param_header)
        
        # Table des paramètres
        self.param_table = QTableWidget(3, 2)
        self.param_table.setHorizontalHeaderLabels(["Clé", "Valeur"])
        self.param_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.param_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.param_table.verticalHeader().setVisible(False)
        self.param_table.setAlternatingRowColors(True)
        
        self.params_layout.addWidget(self.param_table)
        
        # Tab pour les headers
        self.headers_tab = QWidget()
        self.headers_layout = QVBoxLayout(self.headers_tab)
        
        self.header_table_header = QHBoxLayout()
        self.header_table_title = QLabel("Headers")
        self.add_header_button = QPushButton("+")
        self.add_header_button.setFixedSize(24, 24)
        self.add_header_button.clicked.connect(self.add_header_row)
        
        self.header_table_header.addWidget(self.header_table_title)
        self.header_table_header.addStretch()
        self.header_table_header.addWidget(self.add_header_button)
        
        self.headers_layout.addLayout(self.header_table_header)
        
        # Table des headers
        self.header_table = QTableWidget(3, 2)
        self.header_table.setHorizontalHeaderLabels(["Clé", "Valeur"])
        self.header_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.header_table.verticalHeader().setVisible(False)
        self.header_table.setAlternatingRowColors(True)
        
        self.headers_layout.addWidget(self.header_table)
        
        # Tab pour les cookies
        self.cookies_tab = QWidget()
        self.cookies_layout = QVBoxLayout(self.cookies_tab)
        
        self.cookie_table_header = QHBoxLayout()
        self.cookie_table_title = QLabel("Cookies")
        self.add_cookie_button = QPushButton("+")
        self.add_cookie_button.setFixedSize(24, 24)
        self.add_cookie_button.clicked.connect(self.add_cookie_row)
        
        self.cookie_table_header.addWidget(self.cookie_table_title)
        self.cookie_table_header.addStretch()
        self.cookie_table_header.addWidget(self.add_cookie_button)
        
        self.cookies_layout.addLayout(self.cookie_table_header)
        
        # Table des cookies
        self.cookie_table = QTableWidget(3, 2)
        self.cookie_table.setHorizontalHeaderLabels(["Clé", "Valeur"])
        self.cookie_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cookie_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cookie_table.verticalHeader().setVisible(False)
        self.cookie_table.setAlternatingRowColors(True)
        
        self.cookies_layout.addWidget(self.cookie_table)
        
        # Tab pour les données POST
        self.post_data_tab = QWidget()
        self.post_data_layout = QVBoxLayout(self.post_data_tab)
        
        self.post_data_type_layout = QHBoxLayout()
        self.post_data_type_label = QLabel("Type de données:")
        self.post_data_type_combo = QComboBox()
        self.post_data_type_combo.addItems(["form-data", "x-www-form-urlencoded", "raw", "binary"])
        self.post_data_type_combo.currentIndexChanged.connect(self.update_post_data_ui)
        
        self.post_data_type_layout.addWidget(self.post_data_type_label)
        self.post_data_type_layout.addWidget(self.post_data_type_combo)
        self.post_data_type_layout.addStretch()
        
        self.post_data_layout.addLayout(self.post_data_type_layout)
        
        # Stack pour les différents types de données POST
        self.post_data_stack = QStackedWidget()
        
        # Form-data
        self.form_data_widget = QWidget()
        self.form_data_layout = QVBoxLayout(self.form_data_widget)
        
        self.form_data_header = QHBoxLayout()
        self.form_data_title = QLabel("Form Data")
        self.add_form_data_button = QPushButton("+")
        self.add_form_data_button.setFixedSize(24, 24)
        self.add_form_data_button.clicked.connect(self.add_form_data_row)
        
        self.form_data_header.addWidget(self.form_data_title)
        self.form_data_header.addStretch()
        self.form_data_header.addWidget(self.add_form_data_button)
        
        self.form_data_layout.addLayout(self.form_data_header)
        
        self.form_data_table = QTableWidget(3, 2)
        self.form_data_table.setHorizontalHeaderLabels(["Clé", "Valeur"])
        self.form_data_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.form_data_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.form_data_table.verticalHeader().setVisible(False)
        self.form_data_table.setAlternatingRowColors(True)
        
        self.form_data_layout.addWidget(self.form_data_table)
        
        # Raw data
        self.raw_data_widget = QWidget()
        self.raw_data_layout = QVBoxLayout(self.raw_data_widget)
        
        self.raw_data_format_layout = QHBoxLayout()
        self.raw_data_format_label = QLabel("Format:")
        self.raw_data_format_combo = QComboBox()
        self.raw_data_format_combo.addItems(["JSON", "XML", "HTML", "Text"])
        
        self.raw_data_format_layout.addWidget(self.raw_data_format_label)
        self.raw_data_format_layout.addWidget(self.raw_data_format_combo)
        self.raw_data_format_layout.addStretch()
        
        self.raw_data_layout.addLayout(self.raw_data_format_layout)
        
        self.raw_data_editor = QTextEdit()
        self.raw_data_editor.setPlaceholderText("Entrez les données brutes ici...")
        self.raw_data_editor.setAcceptRichText(False)
        self.raw_data_editor.setFont(QFont("Consolas", 10))
        
        self.raw_data_layout.addWidget(self.raw_data_editor)
        
        # Binary data
        self.binary_data_widget = QWidget()
        self.binary_data_layout = QVBoxLayout(self.binary_data_widget)
        
        self.binary_file_path = QLineEdit()
        self.binary_file_path.setReadOnly(True)
        self.binary_file_path.setPlaceholderText("Aucun fichier sélectionné")
        
        self.binary_file_button = QPushButton("Parcourir...")
        self.binary_file_button.clicked.connect(self.select_binary_file)
        
        self.binary_file_layout = QHBoxLayout()
        self.binary_file_layout.addWidget(self.binary_file_path)
        self.binary_file_layout.addWidget(self.binary_file_button)
        
        self.binary_data_layout.addLayout(self.binary_file_layout)
        self.binary_data_layout.addStretch()
        
        # Ajouter les widgets au stack
        self.post_data_stack.addWidget(self.form_data_widget)
        self.post_data_stack.addWidget(self.form_data_widget)  # x-www-form-urlencoded (même UI que form-data)
        self.post_data_stack.addWidget(self.raw_data_widget)
        self.post_data_stack.addWidget(self.binary_data_widget)
        
        self.post_data_layout.addWidget(self.post_data_stack)
        
        # Ajouter les onglets au widget d'onglets
        self.tabs.addTab(self.params_tab, "Paramètres")
        self.tabs.addTab(self.headers_tab, "Headers")
        self.tabs.addTab(self.cookies_tab, "Cookies")
        self.tabs.addTab(self.post_data_tab, "Données POST")
        
        # Bouton d'envoi
        self.send_button = QPushButton("Envoyer la requête")
        self.send_button.clicked.connect(self.send_request)
        
        # Status label
        self.status_label = QLabel("Prêt")
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.status_layout = QHBoxLayout()
        self.status_layout.addWidget(self.status_label)
        self.status_layout.addStretch()
        self.status_layout.addWidget(self.send_button)
        
        # Ajouter les layouts au layout du contenu
        self.content_layout.addLayout(self.url_layout)
        self.content_layout.addWidget(self.tabs)
        self.content_layout.addLayout(self.status_layout)
        
    def add_parameter_row(self):
        current_rows = self.param_table.rowCount()
        self.param_table.setRowCount(current_rows + 1)
        
    def add_header_row(self):
        current_rows = self.header_table.rowCount()
        self.header_table.setRowCount(current_rows + 1)
        
    def add_cookie_row(self):
        current_rows = self.cookie_table.rowCount()
        self.cookie_table.setRowCount(current_rows + 1)
        
    def add_form_data_row(self):
        current_rows = self.form_data_table.rowCount()
        self.form_data_table.setRowCount(current_rows + 1)
        
    def update_post_data_ui(self, index):
        self.post_data_stack.setCurrentIndex(index)
        
    def select_binary_file(self):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier")
        if file_path:
            self.binary_file_path.setText(file_path)
            
    def get_params_from_table(self, table):
        """Récupère les paramètres depuis une table"""
        params = {}
        for row in range(table.rowCount()):
            key_item = table.item(row, 0)
            value_item = table.item(row, 1)
            if key_item and key_item.text() and value_item:
                params[key_item.text()] = value_item.text()
        print(params)
        return params
        
    def get_headers(self):
        return self.get_params_from_table(self.header_table)
        
    def get_cookies(self):
        return self.get_params_from_table(self.cookie_table)
        
    def get_post_data(self):
        index = self.post_data_type_combo.currentIndex()
        if index == 0 or index == 1:  # form-data ou x-www-form-urlencoded
            return self.get_params_from_table(self.form_data_table)
        elif index == 2:  # raw
            return self.raw_data_editor.toPlainText()
        elif index == 3:  # binary
            return self.binary_file_path.text()
        return {}
        
    def send_request(self):
        """Prépare et envoie la requête via l'objet Request"""
        # Animation du bouton
        self.send_button.setEnabled(False)
        self.send_button.setText("Envoi...")
        self.status_label.setText("Envoi en cours...")
        
        # Mettre à jour l'objet Request avec les valeurs de l'interface
        self.request.set_url(self.url_input.text())
        self.request.set_method(self.method_combo.currentText())
        self.request.set_params(self.get_params_from_table(self.param_table))
        self.request.set_headers(self.get_params_from_table(self.header_table))
        self.request.set_cookies(self.get_params_from_table(self.cookie_table))
        
        try:
            self.request.send()
            self.status_label.setText(f"Statut: {self.request.status_code}")
            if 200 <= self.request.status_code < 300:
                self.status_label.setStyleSheet("color: #4CAF50;")
            elif 300 <= self.request.status_code < 400:
                self.status_label.setStyleSheet("color: #2196F3;")
            elif 400 <= self.request.status_code < 500:
                self.status_label.setStyleSheet("color: #FF9800;")
            else:
                self.status_label.setStyleSheet("color: #F44336;")
                
        except Exception as e:
            self.status_label.setText(f"Erreur: {str(e)}")
            self.status_label.setStyleSheet("color: #F44336;")
            
        finally:
            # Réinitialisation du bouton
            self.send_button.setEnabled(True)
            self.send_button.setText("Envoyer la requête")
            
    def get_result(self):
        """Retourne le résultat de la requête"""
        return self.request.last_response
        
    def execute(self):
        """Exécute la requête et retourne son résultat"""
        self.send_request()
        return self.get_result()