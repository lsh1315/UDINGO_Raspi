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
import time

def receive_dwm1000_distance(
    port: str = "/dev/ttyS0",
    baud: int = 115200,
    line_timeout: float = 1.0,  # 타임아웃을 1초로 약간 늘려서 안정성 확보
):
    """
    STM32에서 UART로 오는 'd1,d2,d3,d4\n' 한 줄을 수신해
    (d1, d2, d3, d4) float 튜플로 반환합니다.
    UART 설정: 115200, 8N1, 흐름 제어 없음 (가장 표준적인 설정)
    """
    ser = None # try-finally 블록을 위해 미리 선언
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud,
            timeout=line_timeout,
            bytesize=serial.EIGHTBITS,    # 8-bit
            parity=serial.PARITY_NONE,    # No parity
            stopbits=serial.STOPBITS_ONE, # 1 stop bit
            xonxoff=False,                # No software flow control
            rtscts=False,
            dsrdtr=False,
        )
        ser.reset_input_buffer() # 버퍼 비우기

        while True:
            # 데이터가 들어올 때까지 blocking되며 기다림 (타임아웃 발생 시 빈 바이트 반환)
            raw = ser.readline()
            if not raw:
                print("데이터 수신 타임아웃...")
                continue # 데이터가 없으면 다시 시도

            try:
                # 수신된 바이트를 ascii 문자열로 디코딩
                line = raw.decode("ascii").strip()
                print(f"수신된 원본 데이터: '{line}'") # 디버깅을 위해 수신 데이터 출력
            except UnicodeDecodeError:
                print("ASCII 디코딩 실패. 잘못된 데이터 수신.")
                continue

            # 유효성 검사 (','가 3개인지)
            if line.count(',') != 3:
                continue

            parts = line.split(",")
            try:
                # 4개의 숫자로 변환 시도
                d1, d2, d3, d4 = map(float, parts)
                return (d1, d2, d3, d4)  # 성공 시 즉시 값 반환하고 함수 종료
            except ValueError:
                print(f"'{line}' -> 숫자로 변환 실패.")
                # 숫자 변환 실패 시 다음 라인 대기
                continue
    except serial.SerialException as e:
        print(f"시리얼 포트 에러: {e}")
        return None # 에러 발생 시 None 반환
    finally:
        if ser and ser.is_open:
            ser.close()
            print("시리얼 포트 닫힘.")

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


def run_all_and_print_row_col(port="/dev/ttyS0", baud=115200, line_timeout=1.0):
    print(f"1111111111111")
    distances = receive_dwm1000_distance()
    print(f"2222222222222")
    coords = trilaterate(distances)
    if coords is None:
        return None  # 위치 계산 실패 시 None
    row_col = correction(coords)
    print(f"({row_col[0]}, {row_col[1]})")
    return row_col

if __name__ == "__main__":
    run_all_and_print_row_col(port="/dev/ttyS0", baud=115200, line_timeout=1.0)
