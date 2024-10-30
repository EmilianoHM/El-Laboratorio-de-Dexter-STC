# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QLabel
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from ui.login_screen import LoginScreen
from ui.painter_screen import PainterScreen
from ui.jury_screen import JuryScreen
from ui.president_screen import PresidentScreen
from back.blind_signature import BlindSignatureHelper
import os

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robo-Dexo")
        self.setGeometry(100, 100, 400, 300)

        # Colores
        fondo_logo = QColor("#2F3548")
        naranja = QColor("#FFA726")
        palette = QPalette()
        palette.setColor(QPalette.Window, fondo_logo)
        self.setPalette(palette)

        # Estilo Moderno con QSS
        self.setStyleSheet("""
            QMainWindow { background-color: #2F3548; }
            QLabel#titleLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 5px;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #FFA726;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #FFB84D;
            }
            QLineEdit {
                background-color: #3E475A;
                color: white;
                padding: 8px;
                border: 2px solid #FFA726;
                border-radius: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #FFB84D;
            }
        """)
        
        # Initialize Blind Signature Helper
        self.blind_signature_helper = BlindSignatureHelper()

        # Variables
        self.painting_path = None
        self.evaluation = None
        self.blinded_message = None
        self.blinding_factor = None
        self.signature = None

        # Configuración del widget principal
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Pantallas del sistema
        self.login_screen = LoginScreen(self)
        self.painter_screen = PainterScreen(self)
        self.jury_screen = JuryScreen(self)
        self.president_screen = PresidentScreen(self)

        # Agregar pantallas al widget principal
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.painter_screen)
        self.stacked_widget.addWidget(self.jury_screen)
        self.stacked_widget.addWidget(self.president_screen)

    def logout(self):
        # Método para regresar a la pantalla de inicio de sesión y limpiar datos
        self.painting_path = None
        self.evaluation = None
        self.blinded_message = None
        self.blinding_factor = None
        self.signature = None
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def add_logo(self, layout):
        # Cargar el logo desde la carpeta assets
        logo_path = os.path.join("assets", "robo_dexo_logo.webp")
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
