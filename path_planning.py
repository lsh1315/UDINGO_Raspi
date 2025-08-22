###########################################################
## class 정의 -> main 에서 선언해 사용
##
## 멤버 변수 :
## 1. goal[x,y]
## 2. path[(x1,y1), (x2,y2), ... ]
##
## 멤버 함수 :
## 1. 추천 주차 구역 선정 알고리즘
##      Input : 주차장 배열, 현재 위치 , 빈자리 , 사용자 선호도
##      Output : self.goal 좌표 수정
## 2. A* 알고리즘
##      Input : 주차장 배열, 현재 위치 , 목적지
##      Output : self.path 좌표들 저장
###########################################################

규약
- 맵: lot[y][x] (2D 리스트). 1=벽/장애물, 2~5=주차칸, 6=입구, 7=출구, 8=마트
- 외부 인터페이스: (x, y)  // main과 GUI 에서 쓰는 순서
- 내부 연산은 (y, x)로 처리하고, 입출력 시 (x, y)로 변환

특징
- C 코드와 동일한 A*: open 리스트 선형 검색, 4방향, 맨해튼 휴리스틱, 부모 포인터.
- ARRAY_CAPACITY=100 가드 동일.
- 좌표 혼동 방지: A*가 첫 시도 실패 시 (x,y)<->(y,x) 스왑 재시도.
"""

from __future__ import annotations
from typing import List, Tuple, Iterable, Optional

INF = 99999
ARRAY_CAPACITY_DEFAULT = 100

Coord = Tuple[int, int]

def _manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



class PathPlanning:
    def __init__(self) -> None:
        self.goal: List[int] = [-1, -1]   # [y, x]
        self.path: List[Coord] = []       # [(y,x), ...]

    # ------------------------------------------------------
    # 1) 추천 주차 구역 선정
    # ------------------------------------------------------
    def recommend_parking(
        self,
        lot: List[List[int]],
        current_pos: Coord,
        user_pref: Tuple[int, int],
    ) -> None:
        rows = len(lot)
        cols = len(lot[0]) if rows else 0

        preferred_type, prefer_criteria = user_pref

        # 기준 포인트
        entry = exit_ = mall = (-1, -1)
        for y in range(rows):
            for x in range(cols):
                v = lot[y][x]
                if v == 6:
                    entry = (y, x)
                elif v == 7:
                    exit_ = (y, x)
                elif v == 8 and mall == (-1, -1):
                    mall = (y, x)

        def ref_point() -> Coord:
            if prefer_criteria == 1: return entry
            if prefer_criteria == 2: return exit_
            if prefer_criteria == 3: return mall
            return (-1, -1)

        ref = ref_point()

        def is_candidate(y: int, x: int) -> bool:
            t = lot[y][x]
            return 2 <= t <= 5

        best = (INF, -1, -1)

        # 1) 선호 타입
        for y in range(rows):
            for x in range(cols):
                if not is_candidate(y, x): continue
                if lot[y][x] != preferred_type: continue
                d = _manhattan((y, x), ref) if ref != (-1, -1) else _manhattan((y, x), current_pos)
                if d < best[0]:
                    best = (d, y, x)

        # 2) 없으면 일반(4)
        if best[1] == -1:
            for y in range(rows):
                for x in range(cols):
                    if not is_candidate(y, x): continue
                    if lot[y][x] != 4: continue
                    d = _manhattan((y, x), ref) if ref != (-1, -1) else _manhattan((y, x), current_pos)
                    if d < best[0]:
                        best = (d, y, x)

        if best[1] == -1:
            self.goal = [-1, -1]
        else:
            self.goal = [best[1], best[2]]  # [y, x]

    # ------------------------------------------------------
    # 2) A* 알고리즘
    # ------------------------------------------------------
    def astar(
        self,
        lot: List[List[int]],
        current_pos: Coord,
        goal: Coord,
        array_capacity: int = ARRAY_CAPACITY_DEFAULT,
    ) -> int:
        rows = len(lot)
        cols = len(lot[0]) if rows else 0
        sy, sx = current_pos
        ty, tx = goal

        def in_bounds(y: int, x: int) -> bool:
            return 0 <= y < rows and 0 <= x < cols

        if not (in_bounds(sy, sx) and in_bounds(ty, tx)):
            self.path = []
            return 0

        g = [[INF] * cols for _ in range(rows)]
        f = [[INF] * cols for _ in range(rows)]
        py = [[-1] * cols for _ in range(rows)]
        px = [[-1] * cols for _ in range(rows)]

        g[sy][sx] = 0
        f[sy][sx] = _manhattan((sy, sx), (ty, tx))

        open_list: List[Coord] = [(sy, sx)]
        in_open = [[False] * cols for _ in range(rows)]
        in_open[sy][sx] = True

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while open_list:
            # f 최소
            cur_idx = 0
            cy, cx = open_list[0]
            best_f = f[cy][cx]
            for i in range(1, len(open_list)):
                y, x = open_list[i]
                if f[y][x] < best_f:
                    best_f = f[y][x]
                    cur_idx = i

            cy, cx = open_list[cur_idx]
            open_list[cur_idx] = open_list[-1]
            open_list.pop()
            in_open[cy][cx] = False

            if (cy, cx) == (ty, tx):
                rev: List[Coord] = []
                y, x = ty, tx
                while y != -1 and x != -1:
                    if len(rev) >= array_capacity:
                        self.path = []
                        return 0
                    rev.append((y, x))
                    y, x = py[y][x], px[y][x]
                rev.reverse()
                self.path = rev
                return len(self.path)

            for dy, dx in dirs:
                ny, nx = cy + dy, cx + dx
                if not in_bounds(ny, nx):
                    continue
                if lot[ny][nx] == 1:
                    continue
                tentative_g = g[cy][cx] + 1
                if tentative_g < g[ny][nx]:
                    py[ny][nx] = cy
                    px[ny][nx] = cx
                    g[ny][nx] = tentative_g
                    f[ny][nx] = tentative_g + _manhattan((ny, nx), (ty, tx))
                    if not in_open[ny][nx]:
                        open_list.append((ny, nx))
                        in_open[ny][nx] = True

        self.path = []
        return 0

    def get_goal(self) -> Coord:
        return (self.goal[0], self.goal[1])

    def get_path(self) -> List[Coord]:
        return list(self.path)
