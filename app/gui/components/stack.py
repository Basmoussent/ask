from app.core.bloc import base_bloc
from app.core.bloc.request import RequestBlock
from app.core.bloc.parse import ParseBlock
from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout,
	QPushButton, QScrollArea
)
from PySide6.QtCore import Qt

class BlockStack(QWidget):
	"""Widget pour gérer une pile de blocs"""
	def __init__(self, parent=None):
		super().__init__(parent)
		self.blocks = []
		self.raw_view = None  # Pour stocker la référence au raw_view
		self.init_ui()
		
	def init_ui(self):
		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(5)
		
		# Toolbar
		self.toolbar = QHBoxLayout()
		self.toolbar.setContentsMargins(5, 5, 5, 5)
		
		self.add_block_button = QPushButton("+")
		self.add_block_button.setToolTip("Ajouter un bloc")
		self.add_block_button.clicked.connect(self.show_block_menu)

		self.execute_all_button = QPushButton("▶")
		self.execute_all_button.setToolTip("Exécuter tous les blocs")
		self.execute_all_button.clicked.connect(self.execute_all)
		
		self.toolbar.addWidget(self.add_block_button)
		self.toolbar.addWidget(self.execute_all_button)
		self.toolbar.addStretch()
		
		# Conteneur de blocs avec scroll
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		
		self.blocks_container = QWidget()
		self.blocks_layout = QVBoxLayout(self.blocks_container)
		self.blocks_layout.setContentsMargins(5, 5, 5, 5)
		self.blocks_layout.setSpacing(10)
		self.blocks_layout.addStretch()
		
		self.scroll_area.setWidget(self.blocks_container)
		
		# Assembler le layout principal
		self.main_layout.addLayout(self.toolbar)
		self.main_layout.addWidget(self.scroll_area)
		
	def show_block_menu(self):
		"""Affiche un menu pour choisir le type de bloc à ajouter"""
		from PySide6.QtWidgets import QMenu
		from PySide6.QtCore import QPoint
		
		menu = QMenu(self)
		add_request_action = menu.addAction("Requête HTTP")
		add_parse_action = menu.addAction("Extraction de valeur")
		
		action = menu.exec_(self.add_block_button.mapToGlobal(QPoint(0, self.add_block_button.height())))
		
		if action == add_request_action:
			self.add_request_block()
		elif action == add_parse_action:
			self.add_parse_block()
			
	def add_request_block(self):
		"""Ajoute un bloc de requête à la pile"""
		block = RequestBlock(self)
		self.add_block(block)
		return block
		
	def add_parse_block(self):
		"""Ajoute un bloc d'extraction à la pile"""
		block = ParseBlock(self)
		if self.blocks and isinstance(self.blocks[-1], RequestBlock):
			# Si le bloc précédent est une requête, lier sa réponse
			previous_block = self.blocks[-1]
			block.set_previous_response(previous_block.get_result())
		self.add_block(block)
		return block
		
	def add_block(self, block):
		"""Ajoute un bloc au conteneur"""
		# Ajouter le bloc avant le stretch
		self.blocks_layout.insertWidget(self.blocks_layout.count() - 1, block)
		
		# Connecter le bouton de suppression
		block.delete_button.clicked.connect(lambda: self.remove_block(block))
		
		# Ajouter à la liste des blocs
		self.blocks.append(block)
		
	def remove_block(self, block):
		"""Supprime un bloc de la pile"""
		if block in self.blocks:
			self.blocks_layout.removeWidget(block)
			self.blocks.remove(block)
			block.deleteLater()
	def set_output_view(self, raw_view):
		"""Configure la vue de sortie pour les résultats"""
		self.raw_view = raw_view

	def execute_all(self):
		"""Exécute tous les blocs dans l'ordre"""
		results = []
		previous_result = None
		
		for block in self.blocks:
			if isinstance(block, ParseBlock) and previous_result:
				block.set_previous_response(previous_result)
				
			result = block.execute()
			results.append(result)
			previous_result = result

		# Afficher le résultat du dernier bloc dans raw_view
		if results and self.raw_view:
			last_result = results[-1]
			# Vérifier si le dernier bloc est un bloc de requête pour formater correctement
			if hasattr(block, 'request') and hasattr(block.request, 'content_type'):
				try:
					if "json" in block.request.content_type.lower():
						import json
						# Formater JSON
						json_data = json.loads(last_result)
						formatted_result = json.dumps(json_data, indent=2)
						self.raw_view.setPlainText(formatted_result)
					else:
						# Texte brut
						self.raw_view.setPlainText(str(last_result))
				except:
					# En cas d'erreur de formatage, afficher le texte brut
					self.raw_view.setPlainText(str(last_result))
			else:
				# Si ce n'est pas un bloc de requête, afficher le résultat brut
				self.raw_view.setPlainText(str(last_result))

		return results