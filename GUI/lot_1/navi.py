import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QPixmap
from PySide6.QtCore import Qt, QPoint, QTimer
from .ui_navi import Ui_MainWindow  # pyside6-uic로 생성된 파일
from typing import List, Tuple
from .map import Map

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
        self.ui.car_red.setVisible(False)
        self.ui.car_red_2.setVisible(False)

        # 현재 위치를 담을 좌표
        self.pos_x = 0
        self.pos_y = 0

        # 이전 위치를 담을 좌표 (입구 기준 초기화)
        self.prev_x = 210
        self.prev_y = 691

        # 찍을 경로 좌표
        self.path = []

        # 사용자 선호도
        self.type = 0
        self.near = 0

        # GUI 업데이트 flag
        self.flag = 0

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

    def save_type2(self):
        self.type = 2
        self.ui.stackedWidget.setCurrentIndex(1)
        self.overlay.clear()
    
    def save_type3(self):
        self.type = 3
        self.ui.stackedWidget.setCurrentIndex(1)
        self.overlay.clear()

    def save_type4(self):
        self.type = 4
        self.ui.stackedWidget.setCurrentIndex(1)
        self.overlay.clear()

    def save_type5(self):
        self.type = 5
        self.ui.stackedWidget.setCurrentIndex(1)
        self.overlay.clear()

    def save_near1(self):
        self.flag = 1
        self.near = 1
        self.ui.stackedWidget.setCurrentIndex(2)
        self.real_time_GUI_update()

    def save_near2(self):
        self.flag = 1
        self.near = 2
        self.ui.stackedWidget.setCurrentIndex(2)
        self.real_time_GUI_update()

    def save_near3(self):
        self.flag = 1
        self.near = 3
        self.ui.stackedWidget.setCurrentIndex(2)
        self.real_time_GUI_update()
        

    def real_time_GUI_update(self):
        # 타이머를 사용하여 moving 함수를 주기적으로 호출
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.moving)
        self.timer.start(50)  # 50ms마다 호출 (초당 20회)

    def moving(self):

        # 차 위치 옮기기 Test
        # self.pos_x += 10

        dx = self.pos_x - self.prev_x
        dy = self.pos_y - self.prev_y

        # if dx == 0 and dy == 0:
        #     return

        # path에 담긴 모든 좌표에 빨간 점 출력
        self.overlay.clear()
        self._sync_overlay_geometry()
        self.overlay.set_points(self.path)
        self.overlay.show()
        self.ui.car.move(self.pos_x, self.pos_y)

        if dx > 0 and dy == 0:
            self.ui.car.setPixmap(QPixmap(u":/car/car_90.png"))
        elif dx < 0 and dy == 0:
            self.ui.car.setPixmap(QPixmap(u":/car/car_270.png"))
        elif dx == 0 and dy < 0:
            self.ui.car.setPixmap(QPixmap(u":/car/car_0.png"))
        elif dx == 0 and dy > 0:
            self.ui.car.setPixmap(QPixmap(u":/car/car_180.png"))
        else:
            if abs(dx) > abs(dy):
                if dx > 0 :
                    self.ui.car.setPixmap(QPixmap(u":/car/car_90.png"))
                else:
                    self.ui.car.setPixmap(QPixmap(u":/car/car_270.png"))
            else:
                if dy > 0 :
                    self.ui.car.setPixmap(QPixmap(u":/car/car_180.png"))
                else : 
                    self.ui.car.setPixmap(QPixmap(u":/car/car_0.png"))

        self.ui.car.move(self.pos_x, self.pos_y)
        self.ui.car.setVisible(True)
 
        self.prev_x = self.pos_x
        self.prev_y = self.pos_y

    def transfrom_row2y(self, row):
        return 11.78 * row + 53.98

    def transfrom_col2x(self, col):
        return 10.43 * col + 29.68

    def transform_points(self, points):
        return [(self.transfrom_col2x(col), self.transfrom_row2y(row)) for row, col in points]


# if __name__ == "__main__":

#     Parking_lot = Map()
#     Parking_lot.map_reset()

#     app = QApplication(sys.argv)
#     navi = MainWindow()

#     pos_row = 54
#     pos_col = 25
    
#     path_prev = [
#         (54, 25), (54, 26), (54, 27), (54, 28), (54, 29),
#         (54, 30), (54, 31), (54, 32), (54, 33), (54, 34),
#         (54, 35), (54, 36), (54, 37), (54, 38), (54, 39),
#         (54, 40), (54, 41), (54, 42), (54, 43), (54, 44),
#         (54, 45), (54, 46), (54, 47), (54, 48), (54, 49),
#         (54, 50), (54, 51), (54, 52), (54, 53), (54, 54),
#         (54, 55), (54, 56), (54, 57), (54, 58), (54, 59),
#         (54, 60), (54, 61), (54, 62), (54, 63), (54, 64),
#         (54, 65), (53, 65), (52, 65), (51, 65), (50, 65),
#         (49, 65), (48, 65)
#     ]

#     navi.pos_x = navi.transfrom_col2x(pos_col) - 70  # imgae offset
#     navi.pos_y = navi.transfrom_row2y(pos_row) - 70
#     navi.path = navi.transform_points(path_prev)

#     navi.showFullScreen()  # 전체 화면
#     sys.exit(app.exec())