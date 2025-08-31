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

def receive_dwm1000_distance(
    port: str = "/dev/serial0",
    baud: int = 115200,
    line_timeout: float = 0.5,
):
    """
    STM32에서 UART로 오는 'd1,d2,d3,d4' 문자열을 계속 수신.
    최신값을 d1,d2,d3,d4 변수에 저장.
    """
    ser = serial.Serial(
        port=port,
        baudrate=baud,
        timeout=line_timeout,
        bytesize=serial.SEVENBITS,       # 7 데이터 비트
        parity=serial.PARITY_NONE,       # 패리티 없음
        stopbits=serial.STOPBITS_ONE,    # 1 스톱 비트
        xonxoff=True,                    # XON/XOFF 소프트 플로우 제어
        rtscts=False,
        dsrdtr=False
    )

    ser.reset_input_buffer()

    d1 = d2 = d3 = d4 = None  # 초기값

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
            except ValueError:
                continue

            # 여기서 d1,d2,d3,d4 변수는 항상 최신 값으로 갱신됨
    finally:
        ser.close()

    return d1, d2, d3, d4



def trilaterate(distances):
    """
    Calculates the position of a tagger using trilateration with 4 anchors.
    The anchors are assumed to be at the corners of a 1200x600 rectangle.

    Args:
        distances (list or tuple): A list of 4 distances from the tagger to the anchors,
                                   in the order [d1, d2, d3, d4].
                                   d1: distance to anchor at (0, 0)
                                   d2: distance to anchor at (1200, 0)
                                   d3: distance to anchor at (0, 600)
                                   d4: distance to anchor at (1200, 600)

    Returns:
        numpy.ndarray: The calculated (x, y) coordinates of the tagger.
    """
    d1, d2, d3, d4 = distances

    # Anchor coordinates
    x1, y1 = 0, 0
    x2, y2 = 590, 0
    x3, y3 = 0, 1190
    x4, y4 = 590, 1190

    # Set up the system of linear equations Ax = b
    # We linearize the system by creating equations from all 6 pairs of anchors.
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1)],
        [2 * (x3 - x1), 2 * (y3 - y1)],
        [2 * (x4 - x1), 2 * (y4 - y1)],
        [2 * (x3 - x2), 2 * (y3 - y2)],
        [2 * (x4 - x2), 2 * (y4 - y2)],
        [2 * (x4 - x3), 2 * (y4 - y3)]
    ])

    b = np.array([
        d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2,
        d1**2 - d3**2 - x1**2 + x3**2 - y1**2 + y3**2,
        d1**2 - d4**2 - x1**2 + x4**2 - y1**2 + y4**2,
        d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2,
        d2**2 - d4**2 - x2**2 + x4**2 - y2**2 + y4**2,
        d3**2 - d4**2 - x3**2 + x4**2 - y3**2 + y4**2
    ])

    # Solve for x using the pseudo-inverse (least squares solution)
    # x = (A^T * A)^-1 * A^T * b
    try:
        position = np.linalg.inv(A.T @ A) @ A.T @ b
        return position
    except np.linalg.LinAlgError:
        return None # Cannot compute the position, likely due to collinear points or other issues


def correction(original_position, position):
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
            return

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

if __name__ == "__main__":
    tup = receive_dwm1000_distance()
    print(tup)
