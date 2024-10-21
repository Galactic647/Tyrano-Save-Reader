from ui import TyranoBrowserUI

from PySide2.QtWidgets import QApplication
import sys


class 


def main():
    app = QApplication(sys.argv)
    window = TyranoBrowserUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

