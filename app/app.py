import sys
from PyQt5.QtWidgets import QApplication 

from app.parameterValidation import InputDialogApp
    
    
def main():
    app = QApplication(sys.argv)

    input_window = InputDialogApp()
    input_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()