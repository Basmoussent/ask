from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat
import json

class JsonSyntaxHighlighter(QSyntaxHighlighter):
    """Surlignage de syntaxe simple pour JSON"""
    
    def __init__(self, document):
        super().__init__(document)
        
        # Formats de texte pour différents éléments JSON
        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor("#C77DFF"))  # Violet clair
        self.key_format.setFontWeight(QFont.Bold)
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#4CAF50"))  # Vert
        
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#2196F3"))  # Bleu
        
        self.boolean_format = QTextCharFormat()
        self.boolean_format.setForeground(QColor("#FF9800"))  # Orange
        
        self.null_format = QTextCharFormat()
        self.null_format.setForeground(QColor("#F44336"))  # Rouge
        
        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#FFFFFF"))  # Blanc
        self.bracket_format.setFontWeight(QFont.Bold)

    def highlightBlock(self, text):
        """Surligne un bloc de texte JSON"""
        # Surligne les clés (texte entre guillemets suivi de :)
        in_string = False
        start = 0
        for i, char in enumerate(text):
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                if not in_string:  # Début d'une chaîne
                    start = i
                    in_string = True
                else:  # Fin d'une chaîne
                    # Vérifie si c'est une clé (suivi par : après des espaces éventuels)
                    j = i + 1
                    while j < len(text) and text[j].isspace():
                        j += 1
                    
                    if j < len(text) and text[j] == ':':
                        self.setFormat(start, i - start + 1, self.key_format)
                    else:
                        self.setFormat(start, i - start + 1, self.string_format)
                    
                    in_string = False
        
        # Surligne les nombres
        for i, char in enumerate(text):
            if char.isdigit() or char == '-':
                # Vérifie si c'est le début d'un nombre
                if i == 0 or not text[i-1].isalnum():
                    j = i
                    while j < len(text) and (text[j].isdigit() or text[j] in '.-+eE'):
                        j += 1
                    self.setFormat(i, j - i, self.number_format)
        
        # Surligne les mots-clés boolean et null
        keywords = {'true': self.boolean_format, 'false': self.boolean_format, 'null': self.null_format}
        for keyword, format in keywords.items():
            i = 0
            while i <= len(text) - len(keyword):
                if text[i:i+len(keyword)] == keyword:
                    # Vérifie que c'est un mot séparé
                    if (i == 0 or not text[i-1].isalnum()) and (i+len(keyword) == len(text) or not text[i+len(keyword)].isalnum()):
                        self.setFormat(i, len(keyword), format)
                i += 1
        
        # Surligne les crochets et accolades
        for i, char in enumerate(text):
            if char in '[]{}:,':
                self.setFormat(i, 1, self.bracket_format)