##########################################################
## AWS 서버 통신 구현
##
## 현재 주차장에 대한 주차장 정보(빈자리) 요청 및 수집
## 목적지 예약 정보 업로드
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