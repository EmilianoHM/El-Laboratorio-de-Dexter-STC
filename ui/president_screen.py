from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class PresidentScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        layout = QVBoxLayout()

        # Agregar el logo
        self.main_app.add_logo(layout)

        title = QLabel("Bienvenido, Presidente del Jurado")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        validate_button = QPushButton("Validar Evaluación (Firma Ciega)")
        validate_button.clicked.connect(self.blind_signature)
        layout.addWidget(validate_button)

        view_results_button = QPushButton("Ver Resultados")
        view_results_button.clicked.connect(self.view_results)
        layout.addWidget(view_results_button)
        
        logout_button = QPushButton("Salir de la Sesión")
        logout_button.clicked.connect(self.main_app.logout)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def blind_signature(self):
        if self.main_app.blinded_message:
            blinded_signature = self.main_app.blind_signature_helper.sign_message(self.main_app.blinded_message)
            self.main_app.signature = self.main_app.blind_signature_helper.unblind_signature(blinded_signature, self.main_app.blinding_factor)
            QMessageBox.information(self, "Firma Ciega", "Evaluación firmada ciegamente por el presidente")
        else:
            QMessageBox.warning(self, "Error", "No hay evaluación para firmar")

    def view_results(self):
        if self.main_app.evaluation and self.main_app.signature:
            QMessageBox.information(self, "Resultados", f"Evaluación: {self.main_app.evaluation} estrellas, Firma: {self.main_app.signature.hex()}")
        else:
            QMessageBox.warning(self, "Error", "No hay resultados disponibles")
