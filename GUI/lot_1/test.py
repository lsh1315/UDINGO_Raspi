import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_test import Ui_MainWindow   # pyside6-uic로 생성된 파일

class MainWindow(QMainWindow):
    pos_x = 200
    pos_y = 550

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()    # 디자이너 클래스 인스턴스
        self.ui.setupUi(self)        # QMainWindow(self)에 UI 주입
        self.ui.car.setVisible(False)

        # 여기서부터 위젯 접근은 self.ui.객체이름
        # 예) 페이지 전환 버튼 연결:
        # self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        # self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

    def terminate(self):
        self.pos_y -= 10
        self.ui.car.move(self.pos_x, self.pos_y)
        self.ui.car.setVisible(True)

    def next_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # win.show()  # 일반 창
    win.showFullScreen()  # 전체 화면
    sys.exit(app.exec())

