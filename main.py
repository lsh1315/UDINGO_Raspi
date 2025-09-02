import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject, QThread, Slot

from GUI.lot_1.map import Map
from GUI.lot_1.navi import MainWindow
import server_communication as sc
import position_detection as pd
from path_planning import PathPlanning

global user_preference
global position 

pos_row = 48
pos_col = 24

class Worker(QObject):
    """
    GUI와 독립적으로 백그라운드에서 실행될 작업자 클래스.
    """
    def __init__(self):
        super().__init__()
        self.running = True
        self.pos = (pos_row,pos_col)

    @Slot()
    def run(self):
        """
        백그라운드에서 실행될 메인 작업.
        1초마다 "!"를 출력합니다.
        """
        while self.running:
            # 현재 위치 업데이트
            self.pos = pd.run_all_and_print_row_col()    # (self.pos[0]-2, self.pos[1])     # pd.run_all_and_print_row_col()

            # 점유 정보 서버로 부터 수신
            srv.receive_once()          # 문자열 수신
            srv.parse_coordinates()     # 파싱
            for (row,col) in srv.Non_empty_spot:
                Parking_lot.copy_map[row][col] = 1
                if row == 17 and col == 17:
                    navi.ui.car_red.setVisible(True)
                elif row == 30 and col == 17:
                    navi.ui.car_red_2.setVisible(True)

            # 경로 탐색
            Path.recommend_parking(Parking_lot.copy_map, self.pos, (navi.type, navi.near))
            Path.astar(Parking_lot.copy_map, self.pos, Path.goal)

            # GUI 파라미터 저장
            navi.pos_x = navi.transfrom_col2x(self.pos[1]) - 65  # imgae offset
            navi.pos_y = navi.transfrom_row2y(self.pos[0]) - 65
            navi.path = navi.transform_points(Path.path)
            time.sleep(0.2)

    def stop(self):
        """작업 루프를 중지시킵니다."""
        self.running = False

if __name__ == "__main__":
    # 주차장 map 정보
    Parking_lot = Map()
    Parking_lot.map_reset()

    # 목적지, 경로 계산 함수 및 경로 리스트를 갖는 class 선언
    Path = PathPlanning()

    # 서버로부터 점유 구역 정보 수신
    srv = sc.Server("3.39.40.177", 5000)
    srv.receive_once()          # 문자열 수신
    srv.parse_coordinates()     # 파싱
    for (row,col) in srv.Non_empty_spot:
        Parking_lot.copy_map[row][col] = 1

    # Qt 애플리케이션 인스턴스 생성
    app = QApplication(sys.argv)
    navi = MainWindow()

    # 백그라운드 작업을 위한 스레드와 워커 생성
    thread = QThread()
    worker = Worker()

    # 워커를 스레드로 이동
    worker.moveToThread(thread)

    # 스레드가 시작될 때 워커의 run 메서드 실행
    thread.started.connect(worker.run)

    # 스레드 시작
    thread.start()

    # GUI 윈도우 표시
    navi.showFullScreen()

    # Qt 이벤트 루프 시작. 이 코드가 실행되는 동안 백그라운드 스레드가 동작합니다.
    # 이 함수가 반환되면(예: 창을 닫으면) 프로그램이 종료됩니다.
    sys.exit(app.exec())