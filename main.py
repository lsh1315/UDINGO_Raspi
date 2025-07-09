import sys
from PySide6.QtWidgets import QApplication
import importlib

import server_communication as sc
import path_planning as pp
import position_detection as pd

# 전역 변수들
global lot_number
global map_matrix
global position 
global path
global empty

# 주차장 인식
lot_number = 1  # input("원하는 lot 번호를 입력하세요 (예: 1, 2): ")


# 서버에 주차장 정보 요청
module_path = f"GUI.lot_{lot_number}.navi"


# GUI 출력 및 선호도 받기
GUI_module = importlib.import_module(module_path)
map_matrix = getattr(GUI_module, 'map_matrix')     # from GUI.lot_1.navi import map_matrix
Navi = getattr(GUI_module, 'Navi')                 # from GUI.lot_1.navi import Navi


# Thread run : 위치 추정 + path_planning + GUI 새로고침




# GUI 내비게이션 출력
app = QApplication(sys.argv)
window = Navi()
window.show()
sys.exit(app.exec())