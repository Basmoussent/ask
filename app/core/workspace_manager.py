from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
	QPushButton, QComboBox, QTableWidget, QTextEdit, QLabel,
	QHeaderView, QSplitter, QButtonGroup, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.core.request_engine import Request as RequestEngine
from app.gui.components.json import JsonSyntaxHighlighter
from app.gui.components.stack import BlockStack
import json


class RequestWorkspace(QWidget):
	def __init__(self):
		super().__init__()
		self.blocks = []  # Liste pour stocker les blocs
		self.active_block = None  # Bloc actuellement actif
		self.block_stack = BlockStack(self)  # Création de l'instance BlockStack
		self.init_ui()
		
	def init_ui(self):
		"""Initialise l'interface utilisateur"""
		self.setWindowTitle("ASK")
		self.setGeometry(100, 100, 1920, 1080)
		self.main_layout = QVBoxLayout()
		self.main_layout.setSpacing(10)
		self.main_layout.setContentsMargins(15, 15, 15, 15)
		
		# URL et méthode
		self.top_layout = QHBoxLayout()
		
		# Splitter horizontal pour diviser les paramètres et la réponse
		self.main_splitter = QSplitter(Qt.Horizontal)
		
		# Section de gauche pour la stack de blocs
		self.left_widget = QWidget()
		self.left_layout = QVBoxLayout(self.left_widget)
		self.left_layout.setContentsMargins(0, 0, 0, 0)
		self.left_layout.addWidget(self.block_stack)
		
		# Section du milieu pour les paramètres
		self.middle_widget = QWidget()
		self.middle_layout = QVBoxLayout(self.middle_widget)
		self.middle_layout.setContentsMargins(0, 0, 0, 0)
		
		self.param_header = QHBoxLayout()
		self.param_title = QLabel("Paramètres")
		self.add_param_button = QPushButton("+")
		self.add_param_button.setFixedSize(30, 30)
		self.add_param_button.clicked.connect(self.add_parameter_row)
		
		self.param_header.addWidget(self.param_title)
		self.param_header.addStretch()
		self.param_header.addWidget(self.add_param_button)
		
		self.middle_layout.addLayout(self.param_header)
		
		# Table des paramètres
		self.param_table = QTableWidget(5, 2)
		self.param_table.setHorizontalHeaderLabels(["Clé", "Valeur"])
		self.param_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.param_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
		self.param_table.verticalHeader().setVisible(False)
		self.param_table.setAlternatingRowColors(True)
		
		self.middle_layout.addWidget(self.param_table)
		
		# Panneau de droite pour la réponse
		self.right_widget = QWidget()
		self.right_layout = QVBoxLayout(self.right_widget)
		self.right_layout.setContentsMargins(0, 0, 0, 0)
		
		# En-tête du panneau de réponse avec boutons de bascule
		self.response_header = QHBoxLayout()
		
		self.response_title = QLabel("Réponse")
		self.status_label = QLabel("")
		self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		
		# Boutons pour basculer entre la vue brute et la prévisualisation
		self.view_buttons_layout = QHBoxLayout()
		self.raw_button = QPushButton("Brut")
		self.raw_button.setCheckable(True)
		self.raw_button.setChecked(True)
		self.preview_button = QPushButton("Prévisualisation")
		self.preview_button.setCheckable(True)
		
		# Groupe de boutons pour assurer qu'un seul est actif à la fois
		self.view_button_group = QButtonGroup()
		self.view_button_group.addButton(self.raw_button)
		self.view_button_group.addButton(self.preview_button)
		self.view_button_group.setExclusive(True)
		self.view_button_group.buttonClicked.connect(self.toggle_view)
		
		self.view_buttons_layout.addWidget(self.raw_button)
		self.view_buttons_layout.addWidget(self.preview_button)
		
		self.response_header.addWidget(self.response_title)
		self.response_header.addStretch()
		self.response_header.addLayout(self.view_buttons_layout)
		self.response_header.addWidget(self.status_label)
		
		self.right_layout.addLayout(self.response_header)
		
		# Widget empilé pour contenir les différentes vues de réponse
		self.response_stack = QStackedWidget()
		
		# Vue brute (texte)
		self.raw_view = QTextEdit()
		self.raw_view.setReadOnly(True)
		self.raw_view.setLineWrapMode(QTextEdit.WidgetWidth)
		self.raw_view.setFont(QFont("Consolas", 10))
		
		# Passer la référence au BlockStack
		self.block_stack.set_output_view(self.raw_view)
		
		# Vue de prévisualisation (texte amélioré avec surlignage)
		self.preview_view = QTextEdit()
		self.preview_view.setReadOnly(True)
		self.preview_view.setLineWrapMode(QTextEdit.WidgetWidth)
		self.preview_view.setFont(QFont("Consolas", 10))
		
		# Créer un surlignage de syntaxe pour JSON
		self.highlighter = JsonSyntaxHighlighter(self.preview_view.document())
		
		# Ajouter les vues à la pile
		self.response_stack.addWidget(self.raw_view)
		self.response_stack.addWidget(self.preview_view)
		
		self.right_layout.addWidget(self.response_stack)
		
		# Ajouter les trois sections au splitter
		self.main_splitter.addWidget(self.left_widget)
		# self.main_splitter.addWidget(self.middle_widget)
		self.main_splitter.addWidget(self.right_widget)
		
		# Définir les tailles relatives des sections
		self.main_splitter.setSizes([300, 300, 400])
		
		# Assemblage final
		self.main_layout.addWidget(self.main_splitter)
		
		self.setLayout(self.main_layout)
		
	def add_parameter_row(self):
		"""Ajoute une nouvelle ligne de paramètres"""
		current_rows = self.param_table.rowCount()
		self.param_table.setRowCount(current_rows + 1)
	
	def toggle_view(self, button):
		print("Toggle view button clicked")
		if button in [self.raw_button, self.preview_button]:
			self.response_stack.setCurrentIndex(0)
			self.response_mode = 0
			# Parcours des blocs de la pile à l'envers pour trouver la dernière requête valide
			for bloc in reversed(self.block_stack.blocks):
				print(f"Checking block: {bloc.title}")
				if hasattr(bloc, "request") and hasattr(bloc.request, "last_response") and bloc.request.last_response:
					self.update_preview_view(bloc)
					break
			
		

	def update_preview_view(self, req):
		"""Mettre à jour la vue de prévisualisation en fonction du type de contenu"""
		self.preview_view.setAcceptRichText(False)
		# Réinitialiser les propriétés pour éviter des problèmes de formatage
		if "json" in req.request.content_type.lower():
			# Formatage JSON pour surlignage
			try:
				json_data = json.loads(req.request.last_response)
				formatted_json = json.dumps(json_data, indent=2)
				self.preview_view.setPlainText(formatted_json)
			except Exception as e:
				print(f"Erreur de formatage JSON: {e}")
				self.preview_view.setPlainText(req.request.last_response)
		
		elif "xml" in req.request.content_type.lower():
			# Formatage XML basique
			try:
				import xml.dom.minidom as md
				xml_dom = md.parseString(req.request.last_response)
				formatted_xml = xml_dom.toprettyxml(indent="  ")
				self.preview_view.setPlainText(formatted_xml)
			except Exception as e:
				print(f"Erreur de formatage XML: {e}")
				self.preview_view.setPlainText(req.request.last_response)
		
		elif "html" in req.request.content_type.lower() and self.response_mode == 1:
			# Pour le HTML, activer le mode rich text
			print("HTML content detected")
			self.preview_view.setPlainText(req.request.last_response)
		
		else:
			# Texte brut
			print("Plain text content detected")
			self.raw_view.setPlainText(req.request.last_response)
				
	def get_params_from_ui(self):
		"""Récupère les paramètres depuis l'interface utilisateur"""
		params = {}
		for row in range(self.param_table.rowCount()):
			key_item = self.param_table.item(row, 0)
			value_item = self.param_table.item(row, 1)
			if key_item and key_item.text() and value_item:
				params[key_item.text()] = value_item.text()
		return params
		
	def send_request(self):
		"""Prépare et envoie la requête via l'objet Request"""
		# Animation du bouton
		self.send_button.setEnabled(False)
		self.send_button.setText("Envoi...")
		
		# Mettre à jour l'objet Request avec les valeurs de l'interface
		self.request.set_url(self.url_input.text())
		self.request.set_method(self.method_combo.currentText())
		self.request.set_params(self.get_params_from_ui())
		
		try:
			# Exécuter tous les blocs de la stack avant d'envoyer la requête
			self.block_stack.execute_all()
			
			# Envoyer la requête
			self.request.send()
			
			# Formatage et affichage du code de statut
			self.status_label.setText(f"Statut: {self.request.status_code}")
			
			# Couleur du statut selon le code
			if 200 <= self.request.status_code < 300:
				self.status_label.setStyleSheet("color: #4CAF50;")  # Vert pour succès
			elif 300 <= self.request.status_code < 400:
				self.status_label.setStyleSheet("color: #2196F3;")  # Bleu pour redirection
			elif 400 <= self.request.status_code < 500:
				self.status_label.setStyleSheet("color: #FF9800;")  # Orange pour erreur client
			else:
				self.status_label.setStyleSheet("color: #F44336;")  # Rouge pour erreur serveur
			
			# Affichage dans la vue brute
			try:
				if "json" in self.request.content_type.lower():
					# Formater JSON
					json_response = json.loads(self.request.last_response)
					formatted_response = json.dumps(json_response, indent=2)
					self.raw_view.setText(formatted_response)
				else:
					# Texte brut
					self.raw_view.setText(self.request.last_response)
			except:
				# Si le formatage échoue, afficher le texte brut
				self.raw_view.setText(self.request.last_response)
			
			# Mettre à jour la prévisualisation si elle est active
			if self.response_stack.currentIndex() == 1:
				self.update_preview_view()
			
		except Exception as e:
			self.raw_view.setText(f"Erreur: {str(e)}")
			self.status_label.setText("Erreur")
			self.status_label.setStyleSheet("color: #F44336;")
			
			# Réinitialiser la prévisualisation
			self.preview_view.setText(self.request.last_response)
		
		finally:
			# Réinitialisation du bouton
			self.send_button.setEnabled(True)
			self.send_button.setText("Envoyer")

	# Nouvelles méthodes pour la gestion des blocs
	def add_block(self, block):
		"""Ajoute un nouveau bloc au workspace"""
		self.blocks.append(block)
		
	def remove_block(self, block_id):
		"""Supprime un bloc du workspace"""
		self.blocks = [b for b in self.blocks if b.id != block_id]
		if self.active_block and self.active_block.id == block_id:
			self.active_block = None

	def set_active_block(self, block):
		"""Définit le bloc actif"""
		self.active_block = block

	def get_active_block(self):
		"""Retourne le bloc actif"""
		return self.active_block

	def get_all_blocks(self):
		"""Retourne tous les blocs"""
		return self.blocks.copy()

	def update_block(self, block_id, updates):
		"""Met à jour un bloc existant"""
		for i, block in enumerate(self.blocks):
			if block.id == block_id:
				self.blocks[i] = {**block, **updates}
				return True
		return False

	def get_block_by_id(self, block_id):
		"""Récupère un bloc par son ID"""
		for block in self.blocks:
			if block.id == block_id:
				return block
		return None

	def has_block(self, block_id):
		"""Vérifie si un bloc existe"""
		return any(block.id == block_id for block in self.blocks)