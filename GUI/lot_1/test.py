import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QTimer
from ui_test import Ui_MainWindow   # pyside6-uic로 생성된 파일

class MainWindow(QMainWindow):
    pos_x = 200
    pos_y = 550

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()    # 디자이너 클래스 인스턴스
        self.ui.setupUi(self)        # QMainWindow(self)에 UI 주입
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.car.setVisible(False)
        

    def terminate(self):
        self.close()

    def moving(self):
        # 차 위치 옮기기 Test
        self.pos_y -= 10
        self.ui.car.move(self.pos_x, self.pos_y)
        self.ui.car.setVisible(True)

    def save_type(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def save_near(self):
        self.ui.stackedWidget.setCurrentIndex(2)

        # 타이머를 사용하여 moving 함수를 주기적으로 호출
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.moving)
        self.timer.start(50)  # 50ms마다 호출 (초당 20회)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # win.show()  # 일반 창
    win.showFullScreen()  # 전체 화면
    sys.exit(app.exec())

