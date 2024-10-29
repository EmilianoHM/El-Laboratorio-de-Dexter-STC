from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox, QFileDialog, QInputDialog
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
import sys
import os

class BlindSignatureHelper:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def blind_message(self, message):
        blinding_factor = os.urandom(32)
        blinded_message = int.from_bytes(message, byteorder='big') * int.from_bytes(blinding_factor, byteorder='big')
        blinded_message = blinded_message.to_bytes((blinded_message.bit_length() + 7) // 8, byteorder='big')
        return blinded_message, blinding_factor

    def sign_message(self, blinded_message):
        # Calcular hash del mensaje cegado
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(blinded_message)
        hash_value = digest.finalize()
        
        # Firma el hash del mensaje cegado
        return self.private_key.sign(
            hash_value,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

    def unblind_signature(self, blinded_signature, blinding_factor):
        signature_int = int.from_bytes(blinded_signature, byteorder='big')
        unblinded_signature = signature_int // int.from_bytes(blinding_factor, byteorder='big')
        return unblinded_signature.to_bytes((unblinded_signature.bit_length() + 7) // 8, byteorder='big')

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
        self.init_login_screen()
        self.init_painter_screen()
        self.init_jury_screen()
        self.init_president_screen()

    def add_logo_with_spacing(self, layout):
        logo_label = QLabel()
        logo_pixmap = QPixmap("robo_dexo_logo.webp").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        layout.addSpacing(10)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

    def init_login_screen(self):
        self.login_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        # Título
        title = QLabel("Inicio de Sesión")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        # Campos de entrada
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de usuario")
        layout.addWidget(self.username_input)
        layout.addSpacing(10)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)

        # Botón de inicio de sesión
        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        layout.addSpacing(10)

        self.login_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.login_screen)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Simulación de autenticación
        if username == "pintor" and password == "123":
            self.stacked_widget.setCurrentWidget(self.painter_screen)
        elif username == "jurado" and password == "123":
            self.stacked_widget.setCurrentWidget(self.jury_screen)
        elif username == "presidente" and password == "123":
            self.stacked_widget.setCurrentWidget(self.president_screen)
        else:
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos")

    def init_painter_screen(self):
        self.painter_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        title = QLabel("Bienvenido, Pintor")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        upload_button = QPushButton("Subir Pintura")
        upload_button.clicked.connect(self.upload_painting)
        layout.addWidget(upload_button)
        layout.addSpacing(10)

        logout_button = QPushButton("Salir de la Sesión")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.painter_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.painter_screen)

    def upload_painting(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecciona una pintura", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.painting_path = file_path
            QMessageBox.information(self, "Éxito", "Pintura subida correctamente")

    def init_jury_screen(self):
        self.jury_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        title = QLabel("Bienvenido, Jurado")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        evaluate_button = QPushButton("Evaluar Pintura")
        evaluate_button.clicked.connect(self.evaluate_painting)
        layout.addWidget(evaluate_button)
        layout.addSpacing(10)

        logout_button = QPushButton("Salir de la Sesión")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.jury_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.jury_screen)

    def evaluate_painting(self):
        if not self.painting_path:
            QMessageBox.warning(self, "Error", "No hay pintura disponible para evaluar")
            return

        text, ok = QInputDialog.getText(self, "Evaluación", "Ingrese la evaluación (1-3 estrellas):")
        if ok and text.isdigit() and 1 <= int(text) <= 3:
            self.evaluation = int(text)
            # Convert evaluation to bytes and blind it
            message = str(self.evaluation).encode()
            self.blinded_message, self.blinding_factor = self.blind_signature_helper.blind_message(message)
            QMessageBox.information(self, "Éxito", "Evaluación registrada y ciega para firma")
        else:
            QMessageBox.warning(self, "Error", "Ingrese una evaluación válida")

    def init_president_screen(self):
        self.president_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        title = QLabel("Bienvenido, Presidente del Jurado")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        validate_button = QPushButton("Validar Evaluación (Firma Ciega)")
        validate_button.clicked.connect(self.blind_signature)
        layout.addWidget(validate_button)
        layout.addSpacing(10)

        view_results_button = QPushButton("Ver Resultados")
        view_results_button.clicked.connect(self.view_results)
        layout.addWidget(view_results_button)
        layout.addSpacing(10)

        logout_button = QPushButton("Salir de la Sesión")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.president_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.president_screen)

    def blind_signature(self):
        if self.blinded_message:
            blinded_signature = self.blind_signature_helper.sign_message(self.blinded_message)
            self.signature = self.blind_signature_helper.unblind_signature(blinded_signature, self.blinding_factor)
            QMessageBox.information(self, "Firma Ciega", "Evaluación firmada ciegamente por el presidente")
        else:
            QMessageBox.warning(self, "Error", "No hay evaluación para firmar")

    def view_results(self):
        if self.evaluation and self.signature:
            QMessageBox.information(self, "Resultados", f"Evaluación: {self.evaluation} estrellas, Firma: {self.signature.hex()}")
        else:
            QMessageBox.warning(self, "Error", "No hay resultados disponibles")

    def logout(self):
        self.username_input.clear()
        self.password_input.clear()
        self.stacked_widget.setCurrentWidget(self.login_screen)

def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
