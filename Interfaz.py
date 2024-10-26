from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QColor, QPalette, QPainter, QBrush
from PyQt5.QtCore import Qt, QRect
import sys

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
        palette.setColor(QPalette.Button, naranja)
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Configuración del widget principal
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Pantallas del sistema
        self.init_login_screen()
        self.init_painter_screen()
        self.init_jury_screen()
        self.init_president_screen()

    def add_logo_with_spacing(self, layout):
        """Función para añadir el logo con espaciado."""
        logo_label = QLabel()
        logo_pixmap = QPixmap("robo_dexo_logo.webp").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_pixmap = self.add_blur_border(logo_pixmap, 15)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        layout.addSpacing(10)  # Espacio debajo del logo

    def init_login_screen(self):
        self.login_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        # Título
        title = QLabel("Inicio de Sesión")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(10)  # Espacio debajo del título

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
        login_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        layout.addSpacing(10)  # Espacio debajo del botón

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
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(10)

        upload_button = QPushButton("Subir Pintura")
        upload_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        layout.addWidget(upload_button)
        layout.addSpacing(10)

        encrypt_button = QPushButton("Cifrar Pintura")
        encrypt_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        layout.addWidget(encrypt_button)
        layout.addSpacing(10)

        logout_button = QPushButton("Salir de la Sesión")
        logout_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.painter_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.painter_screen)

    def init_jury_screen(self):
        self.jury_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        title = QLabel("Bienvenido, Jurado")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(10)

        view_paintings_button = QPushButton("Ver Pinturas Cifradas")
        view_paintings_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        layout.addWidget(view_paintings_button)
        layout.addSpacing(10)

        evaluate_button = QPushButton("Evaluar Pintura")
        evaluate_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        layout.addWidget(evaluate_button)
        layout.addSpacing(10)

        logout_button = QPushButton("Salir de la Sesión")
        logout_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.jury_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.jury_screen)

    def init_president_screen(self):
        self.president_screen = QWidget()
        layout = QVBoxLayout()

        # Añadir logo y espaciado
        self.add_logo_with_spacing(layout)

        title = QLabel("Bienvenido, Presidente del Jurado")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(10)

        validate_button = QPushButton("Validar Evaluación (Firma Ciega)")
        validate_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        layout.addWidget(validate_button)
        layout.addSpacing(10)

        view_results_button = QPushButton("Ver Resultados")
        view_results_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        layout.addWidget(view_results_button)
        layout.addSpacing(10)

        logout_button = QPushButton("Salir de la Sesión")
        logout_button.setStyleSheet("background-color: #FFA726; color: white; font-weight: bold;")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        self.president_screen.setLayout(layout)
        self.stacked_widget.addWidget(self.president_screen)

    def logout(self):
        self.username_input.clear()
        self.password_input.clear()
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def add_blur_border(self, pixmap, radius):
        blurred_pixmap = QPixmap(pixmap.size())
        blurred_pixmap.fill(Qt.transparent)

        painter = QPainter(blurred_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(pixmap))
        painter.drawRoundedRect(QRect(0, 0, pixmap.width(), pixmap.height()), radius, radius)
        painter.end()

        return blurred_pixmap

def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
