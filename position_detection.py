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

# ================================
# 1) 거리 수신 (한 세트 읽고 반환)
# ================================
def receive_dwm1000_distance(
    port: str = "/dev/serial0",
    baud: int = 115200,
    line_timeout: float = 0.5,
):
    """
    STM32에서 UART로 오는 'd1,d2,d3,d4' 문자열을 1회 수신해 float 튜플로 반환.
    - 형식: 공백 없음 (예: 110,600,231,540)
    - UART: 115200, 7N1, XON/XOFF
    """
    ser = serial.Serial(
        port=port,
        baudrate=baud,
        timeout=line_timeout,
        bytesize=serial.SEVENBITS,     # 7 data bits
        parity=serial.PARITY_NONE,     # N
        stopbits=serial.STOPBITS_ONE,  # 1
        xonxoff=True,                  # Software flow control
        rtscts=False,
        dsrdtr=False,
    )
    ser.reset_input_buffer()
    try:
        while True:
            raw = ser.readline()
            if not raw:
                continue
            try:
                line = raw.decode("ascii").strip()
            except Exception:
                continue

            parts = line.split(",")
            if len(parts) != 4:
                continue

            try:
                d1, d2, d3, d4 = map(float, parts)
                return (d1, d2, d3, d4)
            except ValueError:
                # 숫자 변환 실패 시 다음 라인 대기
                continue
    finally:
        ser.close()

# ================================
# 2) 삼변측량
# ================================
def trilaterate(distances):
    """
    4개 앵커와의 거리로 (x, y) 위치 추정.
    distances = (d1, d2, d3, d4)
    앵커 좌표: (0,0), (590,0), (0,1190), (590,1190)
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

    # 수치 안정성을 위해 lstsq 사용
    try:
        pos, *_ = np.linalg.lstsq(A, b, rcond=None)  # shape (2,)
        return (float(pos[0]), float(pos[1]))
    except np.linalg.LinAlgError:
        return None

# ================================
# 3) 보정 (C 로직 그대로, 튜플 반환)
# ================================
def correction(original_position):
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

# ================================
# 4) 통합 함수 (1회 수행)
# ================================
def get_corrected_position(port="/dev/serial0", baud=115200, line_timeout=0.5):
    """
    UART에서 거리 1세트 수신 → (x,y) 추정 → 보정 → 최종 (row,col) 반환.
    실패 시 None 반환.
    """
    distances = receive_dwm1000_distance(port=port, baud=baud, line_timeout=line_timeout)
    coords = trilaterate(distances)
    if coords is None:
        return None
    x, y = coords
    return correction((x, y))

# 예시:
# pos = get_corrected_position("/dev/serial0", 115200)
# print(pos)
