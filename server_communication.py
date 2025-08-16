##########################################################
## Server class 정의 -> main 에서 선언해 사용
##      
## 멤버 변수 : 
## 1. str
## 2. Non_empty_spot[]
##
## 멤버 함수 :
## 1. AWS 서버 통신
##      Output : self.str 저장
## 2. 좌표 파싱 : 
##      Input : self.str
##      Output : self.Non_empty_spot 좌표들 저장
##########################################################

import socket

HOST = '3.39.40.177'  # 서버 IP
PORT = 5000           # 서버 포트

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"서버에 연결됨: {HOST}:{PORT}")

    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(f"[수신] {data.decode(errors='ignore').strip()}")
    except Exception as e:
        print("에러 발생:", e)
