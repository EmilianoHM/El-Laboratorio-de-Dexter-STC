from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt

class JuryScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        layout = QVBoxLayout()

        # Agregar el logo
        self.main_app.add_logo(layout)

        title = QLabel("Bienvenido, Jurado")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        evaluate_button = QPushButton("Evaluar Pintura")
        evaluate_button.clicked.connect(self.evaluate_painting)
        layout.addWidget(evaluate_button)
        
        logout_button = QPushButton("Salir de la Sesión")
        logout_button.clicked.connect(self.main_app.logout)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def evaluate_painting(self):
        if not self.main_app.painting_path:
            QMessageBox.warning(self, "Error", "No hay pintura disponible para evaluar")
            return

        text, ok = QInputDialog.getText(self, "Evaluación", "Ingrese la evaluación (1-3 estrellas):")
        if ok and text.isdigit() and 1 <= int(text) <= 3:
            self.main_app.evaluation = int(text)
            message = str(self.main_app.evaluation).encode()
            self.main_app.blinded_message, self.main_app.blinding_factor = self.main_app.blind_signature_helper.blind_message(message)
            QMessageBox.information(self, "Éxito", "Evaluación registrada y ciega para firma")
        else:
            QMessageBox.warning(self, "Error", "Ingrese una evaluación válida")
