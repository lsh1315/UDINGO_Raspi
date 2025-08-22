##########################################################
## Server class 정의 -> main 에서 선언해 사용
##
## 멤버 변수 :
## 1. str : 서버에서 수신한 문자열
## 2. Non_empty_spot[] : 파싱된 좌표 리스트
##
## 멤버 함수 :
## 1. AWS 서버 통신
##      Output : self.str 저장
## 2. 좌표 파싱 :
##      Input : self.str
##      Output : self.Non_empty_spot 좌표들 저장
##########################################################

import socket
from typing import List, Tuple

Coord = Tuple[int, int]


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.str: str = ""                  # 1. str
        self.Non_empty_spot: List[Coord] = []  # 2. Non_empty_spot[]

    # 1) AWS 서버 통신
    def receive_once(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            data = s.recv(4096)
            self.str = data.decode(errors="ignore").strip()

    # 2) 좌표 파싱
    def parse_coordinates(self) -> None:
        self.Non_empty_spot.clear()
        if not self.str:
            return
        for pair in self.str.split(";"):
            if not pair.strip():
                continue
            try:
                x_str, y_str = pair.split(",")
                self.Non_empty_spot.append((int(x_str), int(y_str)))
            except ValueError:
                continue


# -------------------- 사용 하는법(main에 추가할거?) --------------------
if __name__ == "__main__":
    srv = Server("3.39.40.177", 5000)
    srv.receive_once()
    print("[수신 문자열]:", srv.str)

    srv.parse_coordinates()
    print("[좌표 리스트]:", srv.Non_empty_spot)
