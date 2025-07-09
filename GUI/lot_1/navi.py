import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from .ui_navi import Ui_MainWindow  # Qt Designer로 변환한 클래스 import

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