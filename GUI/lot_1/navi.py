import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from .ui_navi import Ui_MainWindow  # Qt Designer로 변환한 클래스 import
from .ui_screen1 import Ui_MainWindow as Ui_Screen1  # Qt Designer로 변환한 클래스 import
from .ui_screen2 import Ui_MainWindow as Ui_Screen2  # Qt Designer로 변환한 클래스 import
from .ui_screen3 import Ui_MainWindow as Ui_Screen3  # Qt Designer로 변환한 클래스 import
from .ui_screen4 import Ui_MainWindow as Ui_Screen4  # Qt Designer로 변환한 클래스 import

map_matrix = [
    [1,2,3,4],
    [5,6,7,8],
    [9,0,1,2]
    ]

class Navi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # UI 구성요소를 현재 창에 적용

class Screen1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Screen1()
        self.ui.setupUi(self)

    def next_screen(self):
        self.close()
        self.next_window = Screen2()
        self.next_window.show()


class Screen2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Screen2()
        self.ui.setupUi(self)

    def next_screen(self):
        self.close()
        self.next_window = Screen3()
        self.next_window.show()

class Screen3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Screen3()
        self.ui.setupUi(self)

    def next_screen(self):
        self.close()
        self.next_window = Screen4()
        self.next_window.show()

class Screen4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Screen4()
        self.ui.setupUi(self)

    def next_screen(self):
        self.close()
        self.next_window = Navi()
        self.next_window.show()