from PyQt5.QtWidgets import QApplication
from ui.main_window import MainApp
import sys

def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
