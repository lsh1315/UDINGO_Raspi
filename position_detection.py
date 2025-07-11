#######################################################################
## STM32 보드와의 UART 통신 --> 4개의 앵커까지의 거리 수집 (+ 주차장 정보 수집)
## 삼변측량법 기반 현재 위치 추정 알고리즘
##
## Output : 현재 위치 (+ 주차장 정보)
########################################################################
import numpy as np

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
    x2, y2 = 1200, 0
    x3, y3 = 0, 600
    x4, y4 = 1200, 600

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