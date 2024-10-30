from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        layout = QVBoxLayout()

        # Agregar el logo
        self.main_app.add_logo(layout)
        
        title = QLabel("Inicio de Sesión")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de usuario")
        layout.addWidget(self.username_input)
        layout.addSpacing(10)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)

        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "pintor" and password == "123":
            self.main_app.stacked_widget.setCurrentWidget(self.main_app.painter_screen)
        elif username == "jurado" and password == "123":
            self.main_app.stacked_widget.setCurrentWidget(self.main_app.jury_screen)
        elif username == "presidente" and password == "123":
            self.main_app.stacked_widget.setCurrentWidget(self.main_app.president_screen)
        else:
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos")
