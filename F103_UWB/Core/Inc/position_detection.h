#ifndef POSITION_DETECTION_H
#define POSITION_DETECTION_H

/*
 * @brief 4개의 앵커로부터의 거리 값을 이용해 삼변측량으로 위치를 계산합니다.
 * @param distances 4개의 앵커로부터의 거리 값을 담은 double형 배열
 * @param position 계산된 x, y 좌표를 저장할 int형 배열 (크기 2)
 * @return 성공 시 1, 실패 시 0을 반환합니다.
 */
int trilaterate(int distances[4], uint8_t position[2]);

/*
 * @brief UWB 통신을 통해 거리 값을 받아옵니다.
 * @param distances 4개의 앵커로부터의 거리 값을 담은 double형 배열
 */
int receive_dwm1000_distances(int distances[4]);

/*
 * @brief UWB 통신을 통해 거리 값을 받아오고, 삼변측량을 통해 현재 위치를 계산하는 전체 과정을 포함하는 함수입니다.
 * @param position 계산된 x, y 좌표를 저장할 포인터 배열
 */
int update_current_position(uint8_t position[2]);

/*
 * @brief 추정된 좌표를 경로상의 좌표로 보정
 * @param position 계산된 x, y 좌표를 저장할 포인터 배열
 */
void correction(uint8_t original_position[2], uint8_t position[2]);

#endif // POSITION_DETECTION_H
