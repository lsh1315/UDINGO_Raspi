import sys
from PySide6.QtWidgets import QApplication
import importlib

from GUI.lot_1.map import Map
from GUI.lot_1.navi import MainWindow
# import server_communication as sc
# import position_detection as pd
from path_planning import PathPlanning

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

navi.showFullScreen()

pos_row = 36
pos_col = 24
user_preference = (3,3)

# while(1):

Path.recommend_parking(Parking_lot.copy_map, (pos_row,pos_col), user_preference)
Path.astar(Parking_lot.copy_map, (pos_row,pos_col), Path.goal)

navi.pos_x = navi.transfrom_col2x(pos_col) - 65  # imgae offset
navi.pos_y = navi.transfrom_row2y(pos_row) - 65
navi.path = navi.transform_points(Path.path)


# GUI 내비게이션 출력

sys.exit(app.exec())