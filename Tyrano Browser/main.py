from ui import TyranoBrowser

from PySide2.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = TyranoBrowser()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

