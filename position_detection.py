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
import time
import serial  # pip install pyserial

def stream_dwm1000_distances(
    port: str = "/dev/serial0",
    baud: int = 115200,
    line_timeout: float = 0.2,
):
    """
    STM32 보드에서 오는 UART 문자열 "d1,d2,d3,d4"를 계속 읽어
    (d1, d2, d3, d4) float 튜플로 yield 합니다.
    
    - 문자열 형식은 반드시 "숫자,숫자,숫자,숫자" (공백 불허)
    - 예: 110,600,231,540
    """
    with serial.Serial(port=port, baudrate=baud, timeout=line_timeout) as ser:
        ser.reset_input_buffer()
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
                continue  # 형식 불일치 → 버림

            try:
                d1, d2, d3, d4 = map(float, parts)
                yield (d1, d2, d3, d4)
            except ValueError:
                continue

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
