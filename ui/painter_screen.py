from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class PainterScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        layout = QVBoxLayout()

        # Agregar el logo
        self.main_app.add_logo(layout)

        title = QLabel("Bienvenido, Pintor")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        upload_button = QPushButton("Subir Pintura")
        upload_button.clicked.connect(self.upload_painting)
        layout.addWidget(upload_button)
        
        logout_button = QPushButton("Salir de la Sesión")
        logout_button.clicked.connect(self.main_app.logout)
        layout.addWidget(logout_button)

        self.setLayout(layout)

    def upload_painting(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecciona una pintura", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.main_app.painting_path = file_path
            QMessageBox.information(self, "Éxito", "Pintura subida correctamente")
