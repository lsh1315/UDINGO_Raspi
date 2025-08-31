############################################################################################
## receive_dwm1000_distance : STM32 보드와의 UART 통신(문자열 수신) --> 4개의 앵커까지의 거리 저장
##      Output : d1, d2, d3, d4
##
## trilaterate: 삼변측량법 기반 현재 위치 추정 알고리즘(4개)
##      Input : d1, d2, d3, d4
##      Output : x, y
##
## correction : 위치 보정 알고리즘
##      Input : x, y
##      Output : x, y
############################################################################################
import numpy as np
import serial

def receive_dwm1000_distance():
    # 직렬 포트 설정
    # 포트 이름: '/dev/ttyS0' 또는 '/dev/serial0' 일 수 있습니다.
    # Baudrate: 통신 속도 (상대 장치와 동일하게 설정해야 합니다)
    try:
        ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
        ser.flush() # 포트의 입력 버퍼를 비웁니다.
        print("UART 수신을 시작합니다. Ctrl+C를 눌러 종료하세요.")

        while True:
            # 데이터가 들어왔는지 확인
            if ser.in_waiting > 0:
                # 들어온 데이터를 한 줄 읽습니다. (b'\r\n'가 나올 때까지)
                # decode('utf-8')을 사용하여 바이트 데이터를 문자열로 변환합니다.
                # rstrip()으로 끝에 붙는 개행 문자를 제거합니다.
                line = ser.readline().decode('utf-8').rstrip()
                print("수신된 데이터: " + line)

            time.sleep(0.1) # CPU 사용량을 줄이기 위해 잠시 대기

    except serial.SerialException as e:
        print(f"시리얼 포트를 여는 데 실패했습니다: {e}")
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("시리얼 포트를 닫았습니다.")

def trilaterate(distances):
    """
    4개 앵커와의 거리로 (x, y) 위치 추정.
    distances = (d1, d2, d3, d4)
    앵커: (0,0), (590,0), (0,1190), (590,1190)
    """
    d1, d2, d3, d4 = distances

    x1, y1 = 0.0,   0.0
    x2, y2 = 590.0, 0.0
    x3, y3 = 0.0,   1190.0
    x4, y4 = 590.0, 1190.0

    A = np.array([
        [2*(x2-x1), 2*(y2-y1)],
        [2*(x3-x1), 2*(y3-y1)],
        [2*(x4-x1), 2*(y4-y1)],
        [2*(x3-x2), 2*(y3-y2)],
        [2*(x4-x2), 2*(y4-y2)],
        [2*(x4-x3), 2*(y4-y3)],
    ], dtype=float)

    b = np.array([
        d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2,
        d1**2 - d3**2 - x1**2 + x3**2 - y1**2 + y3**2,
        d1**2 - d4**2 - x1**2 + x4**2 - y1**2 + y4**2,
        d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2,
        d2**2 - d4**2 - x2**2 + x4**2 - y2**2 + y4**2,
        d3**2 - d4**2 - x3**2 + x4**2 - y3**2 + y4**2,
    ], dtype=float)

    try:
        pos, *_ = np.linalg.lstsq(A, b, rcond=None)
        return (float(pos[0]), float(pos[1]))
    except Exception:
        return None


def correction(original_position):
    """
    입력: original_position = (x, y)
    출력: (row, col)
    """
    row = original_position[0]
    col = original_position[1]

    if row <= 9:
        if col <= 24:
            row = 9
            col = 24
        elif col > 24 and col < 94:
            row = 9
        else:
            row = 9
            col = 94

    elif row > 9 and row < 54:
        if col <= 24:
            col = 24
        elif col < row + 13 and col < 76 - row and col > 24:
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
            return (row, col)

    elif row >= 54 and row < 60:
        if col <= 24:
            row = 54
            col = 24
        elif col > 24 and col < 94:
            row = 54
        else:
            row = 54
            col = 94
    else:
        return (row, col)

    return (row, col)


def run_all_and_print_row_col(port="/dev/ttyS0", baud=115200, line_timeout=0.5):
    print(f"1111111111111")
    receive_dwm1000_distance()
    print(f"2222222222222")
    coords = trilaterate(distances)
    if coords is None:
        return None  # 위치 계산 실패 시 None
    row_col = correction(coords)
    print(f"({row_col[0]}, {row_col[1]})")
    return row_col

if __name__ == "__main__":
    run_all_and_print_row_col(port="/dev/ttyS0", baud=115200, line_timeout=0.5)
