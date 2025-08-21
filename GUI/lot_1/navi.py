import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QPoint, QTimer
from ui_navi import Ui_MainWindow  # pyside6-uic로 생성된 파일
from typing import List, Tuple
from map import Map

class DotOverlay(QWidget):
    """stackedWidget 위에 덮는 투명 캔버스: points에 있는 좌표를 빨간 점으로 그림"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []
        # 마우스 이벤트 통과 & 배경 투명
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def set_points(self, pts):
        # pts: [(x,y), ...]
        self.points = [QPoint(int(x), int(y)) for (x, y) in pts]
        self.update()

    def clear(self):
        self.points = []
        self.update()

    def paintEvent(self, _):
        if not self.points:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(QPen(Qt.red, 1))
        p.setBrush(QBrush(Qt.red))
        radius = 4  # 점 반경
        for pt in self.points:
            p.drawEllipse(pt, radius, radius)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.car.setVisible(False)

        # 현재 위치를 담을 좌표
        self.pos_x = 0
        self.pos_y = 0

        # 찍을 경로 좌표
        self.path = []

        # stackedWidget 전체를 덮는 투명 오버레이
        self.overlay = DotOverlay(self.ui.stackedWidget)
        self.overlay.setGeometry(self.ui.stackedWidget.rect())
        self.ui.stackedWidget.currentChanged.connect(self._sync_overlay_geometry)

    def _sync_overlay_geometry(self, _index=None):
        # 페이지 전환/리사이즈 시 오버레이 크기 동기화
        self.overlay.setGeometry(self.ui.stackedWidget.rect())
        self.overlay.raise_()  # 항상 최상단

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._sync_overlay_geometry()

    def terminate(self):
        self.close()

    def save_type(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.overlay.clear()

    def save_near(self):
        self.ui.stackedWidget.setCurrentIndex(2)

        # path에 담긴 모든 좌표에 빨간 점 출력
        self._sync_overlay_geometry()
        self.overlay.set_points(self.path)
        self.overlay.show()
        self.ui.car.move(self.pos_x, self.pos_y)
        self.ui.car.setVisible(True)

    #     # 타이머를 사용하여 moving 함수를 주기적으로 호출
    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self.moving)
    #     self.timer.start(50)  # 50ms마다 호출 (초당 20회)

    # def moving(self):
    #     # 차 위치 옮기기 Test
    #     self.pos_y -= 10
    #     self.ui.car.move(self.pos_x, self.pos_y)
    #     self.ui.car.setVisible(True)

    def transform_points(self, points):
        """
        입력: [(x, y), ...] 형태의 좌표 리스트
        처리: (x, y) -> (y, x)로 교환 후
            x' = 10.43 * (y) + 29.68
            y' = 11.78 * (x) + 53.98
        출력: [(x', y'), ...]
        """
        return [(10.43 * y + 29.68, 11.78 * x + 53.98) for x, y in points]


if __name__ == "__main__":

    Parking_lot = Map()
    Parking_lot.map_reset()

    app = QApplication(sys.argv)
    navi = MainWindow()

    pos_row = 54
    pos_col = 25
    
    path_prev = [
        (54, 25), (54, 26), (54, 27), (54, 28), (54, 29),
        (54, 30), (54, 31), (54, 32), (54, 33), (54, 34),
        (54, 35), (54, 36), (54, 37), (54, 38), (54, 39),
        (54, 40), (54, 41), (54, 42), (54, 43), (54, 44),
        (54, 45), (54, 46), (54, 47), (54, 48), (54, 49),
        (54, 50), (54, 51), (54, 52), (54, 53), (54, 54),
        (54, 55), (54, 56), (54, 57), (54, 58), (54, 59),
        (54, 60), (54, 61), (54, 62), (54, 63), (54, 64),
        (54, 65), (53, 65), (52, 65), (51, 65), (50, 65),
        (49, 65), (48, 65)
    ]

    navi.pos_x = 10.43 * pos_col + 29.68 - 31
    navi.pos_y = 11.78 * pos_row + 53.98
    navi.path = navi.transform_points(path_prev)

    navi.showFullScreen()  # 전체 화면
    sys.exit(app.exec())
