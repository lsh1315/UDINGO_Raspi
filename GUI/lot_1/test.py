import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QPoint, QTimer
from ui_test import Ui_MainWindow  # pyside6-uic로 생성된 파일
from typing import List, Tuple

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

        # 초기화
        self.pos_x = 200
        self.pos_y = 550
        # self.path = [
        #     (275, 550), (275, 520), (275, 490), (275, 460), (275, 430),
        #     (275, 400), (275, 370), (275, 340), (275, 310), (275, 280),
        #     (275, 250),
        # ]

        # self.path = self.transform_points(self.apply_correction_with_swap(path_prev))
        self.path = self.transform_points(path_prev)

        # path에 담긴 모든 좌표에 빨간 점 출력
        self._sync_overlay_geometry()
        self.overlay.set_points(self.path)
        self.overlay.show()

        # 타이머를 사용하여 moving 함수를 주기적으로 호출
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.moving)
        self.timer.start(50)  # 50ms마다 호출 (초당 20회)

    def moving(self):
        # 차 위치 옮기기 Test
        self.pos_y -= 10
        self.ui.car.move(self.pos_x, self.pos_y)
        self.ui.car.setVisible(True)

    def transform_points(self, points):
        """
        입력: [(x, y), ...] 형태의 좌표 리스트
        처리: (x, y) -> (y, x)로 교환 후
            x' = 10.43 * (y) + 29.68
            y' = 11.78 * (x) + 53.98
        출력: [(x', y'), ...]
        """
        return [(10.43 * y + 29.68, 11.78 * x + 53.98) for x, y in points]
    
    def correction(self, original_position):
        """주어진 원본 좌표(row, col)를 특정 조건에 따라 보정합니다."""
        row, col = original_position

        # (이전과 동일한 보정 로직)
        if row <= 9:
            if col <= 24:
                row, col = 9, 24
            elif 24 < col < 94:
                row = 9
            else:
                row, col = 9, 94
        elif 9 < row < 54:
            if col <= 24:
                col = 24
            elif 24 < col < row + 13 and col < 76 - row:
                col = 24
            elif row < 30 and col > row + 15 and col > 101 - row:
                row = 9
            elif col > 105 - row and col > row + 42 and col < 94:
                col = 94
            elif col >= 94:
                col = 94
            elif row > 33 and col < 80 - row and col < row + 38:
                row = 54
            else:
                return original_position
        elif 54 <= row < 60:
            if col <= 24:
                row, col = 54, 24
            elif 24 < col < 94:
                row = 54
            else:
                row, col = 54, 94
        else:
            return original_position

        return (row, col)


    def apply_correction_with_swap(self, path):
        """
        경로의 각 좌표(x, y)를 (y, x) 순서로 바꿔 correction() 함수에 적용합니다.

        Args:
            path (list): (x, y) 튜플들이 담긴 리스트.

        Returns:
            list: 모든 좌표에 보정이 적용된 새로운 리스트.
        """
        # for x, y in path: 루프를 돌면서 각 좌표를 x와 y로 받음
        # correction((y, x)): 받은 x, y의 순서를 바꿔서 함수에 전달
        return [self.correction((y, x)) for x, y in path]


path_prev = [
    (58, 25), (57, 25), (56, 25), (55, 25), (54, 25), (53, 25), (52, 25),
    (51, 25), (50, 25), (50, 26), (50, 27), (50, 28), (50, 29), (50, 30),
    (50, 31), (50, 32), (50, 33), (50, 34), (50, 35), (50, 36), (50, 37),
    (50, 38), (50, 39), (50, 40), (50, 41), (50, 42), (50, 43), (50, 44),
    (50, 45), (50, 46), (50, 47), (50, 48), (50, 49), (50, 50), (50, 51),
    (50, 52), (50, 53), (50, 54), (50, 55), (50, 56), (50, 57), (50, 58),
    (50, 59), (49, 59), (49, 60), (49, 61), (49, 62), (49, 63), (49, 64),
    (49, 65), (48, 65)
]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # win.show()  # 일반 창
    win.showFullScreen()  # 전체 화면
    sys.exit(app.exec())
