import sys
from PySide6.QtWidgets import QApplication
import importlib

from GUI.lot_1.map import Map
from GUI.lot_1.navi import MainWindow
# import server_communication as sc
# import position_detection as pd
from .path_planning import PathPlanning

global user_preference
global position 

# 주차장 map 정보
Parking_lot = Map()
Parking_lot.map_reset()

app = QApplication(sys.argv)
navi = MainWindow()

Path = PathPlanning()

# 전역 변수들
# global lot_number

# 주차장 인식
# UWB 통신으로 ID를 받아와서 판단
# lot_number = 1  # input("원하는 lot 번호를 입력하세요 (예: 1, 2): ")

# module_path = f"GUI.lot_{lot_number}.navi"

# GUI 출력 및 선호도 받기
# GUI_module = importlib.import_module(module_path)
# Navi = getattr(GUI_module, 'MainWindow')                 # from GUI.lot_1.navi import Navi
# app = QApplication(sys.argv)
# window = Navi()


# Thread run : 위치 추정 + path_planning + GUI 새로고침
# window.user_function() 으로 새로고침

pos_row = 54
pos_col = 25

Path.recommend_parking(Map.copy_map, (pos_row,pos_col), (2,4))
Path.astar(Map.copy_map, (pos_row,pos_col), Path.goal)

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

navi.pos_x = navi.transfrom_col2x(pos_col) - 70  # imgae offset
navi.pos_y = navi.transfrom_row2y(pos_row) - 70
navi.path = navi.transform_points(path_prev)

# GUI 내비게이션 출력
navi.showFullScreen()
sys.exit(app.exec())