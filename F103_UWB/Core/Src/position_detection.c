#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

// Function to calculate the position using trilateration
// Returns 1 on success, 0 on failure
int trilaterate(int distances[4], uint8_t position[2]) {
    // Anchor coordinates
    double x1 = 10, y1 = 10;
    double x2 = 590, y2 = 10;
    double x3 = 10, y3 = 1190;
    double x4 = 590, y4 = 1190;

    double d1 = distances[0];
    double d2 = distances[1];
    double d3 = distances[2];
    double d4 = distances[3];

    // Matrix A (6x2)
    double A[6][2] = {
        {2 * (x2 - x1), 2 * (y2 - y1)},
        {2 * (x3 - x1), 2 * (y3 - y1)},
        {2 * (x4 - x1), 2 * (y4 - y1)},
        {2 * (x3 - x2), 2 * (y3 - y2)},
        {2 * (x4 - x2), 2 * (y4 - y2)},
        {2 * (x4 - x3), 2 * (y4 - y3)}
    };

    // Vector b (6x1)
    double b[6] = {
        pow(d1, 2) - pow(d2, 2) - pow(x1, 2) + pow(x2, 2) - pow(y1, 2) + pow(y2, 2),
        pow(d1, 2) - pow(d3, 2) - pow(x1, 2) + pow(x3, 2) - pow(y1, 2) + pow(y3, 2),
        pow(d1, 2) - pow(d4, 2) - pow(x1, 2) + pow(x4, 2) - pow(y1, 2) + pow(y4, 2),
        pow(d2, 2) - pow(d3, 2) - pow(x2, 2) + pow(x3, 2) - pow(y2, 2) + pow(y3, 2),
        pow(d2, 2) - pow(d4, 2) - pow(x2, 2) + pow(x4, 2) - pow(y2, 2) + pow(y4, 2),
        pow(d3, 2) - pow(d4, 2) - pow(x3, 2) + pow(x4, 2) - pow(y3, 2) + pow(y4, 2)
    };

    // Transpose of A (A_T is 2x6)
    double A_T[2][6];
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 2; j++) {
            A_T[j][i] = A[i][j];
        }
    }

    // A_T * A (AtA is 2x2)
    double AtA[2][2] = {{0, 0}, {0, 0}};
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 6; k++) {
                AtA[i][j] += A_T[i][k] * A[k][j];
            }
        }
    }

    // A_T * b (Atb is 2x1)
    double Atb[2] = {0, 0};
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 6; j++) {
            Atb[i] += A_T[i][j] * b[j];
        }
    }

    // Inverse of AtA
    // For a 2x2 matrix [[a, b], [c, d]], the inverse is (1/det) * [[d, -b], [-c, a]]
    double det = AtA[0][0] * AtA[1][1] - AtA[0][1] * AtA[1][0];

    if (fabs(det) < 1e-6) { // Check if the determinant is close to zero
        return 0; // Cannot compute the position
    }

    double inv_det = 1.0 / det;
    double AtA_inv[2][2];
    AtA_inv[0][0] = AtA[1][1] * inv_det;
    AtA_inv[0][1] = -AtA[0][1] * inv_det;
    AtA_inv[1][0] = -AtA[1][0] * inv_det;
    AtA_inv[1][1] = AtA[0][0] * inv_det;

    // position = AtA_inv * Atb
    position[0] = (uint8_t)round((AtA_inv[0][0] * Atb[0] + AtA_inv[0][1] * Atb[1])/10); // mm to cm
    position[1] = (uint8_t)round((AtA_inv[1][0] * Atb[0] + AtA_inv[1][1] * Atb[1])/10); // mm to cm

    return 1;
}

int receive_dwm1000_distances(int distances[4]){
    
    // It will be replaced with UART Transceive
    char str[] = "631,250,1114,949";

    char *temp;
    uint8_t i=0;
    temp = strtok(str,",");
    while(temp != NULL){
        distances[i] = atoi(temp);
        if (distances[i] < 0) distances[i] = 0;
        temp = strtok(NULL,",");
        i++;
    }

    return 1;
}

void correction(uint8_t original_position[2], uint8_t position[2]){
    int row = original_position[0];
    int col = original_position[1];

    if (row <= 9){
        if(col <= 24){
            row = 9;
            col = 24;
        }else if(col >24 && col <94){
            row = 9;
        }else{
            row = 9;
            col = 94;
        }
    }else if(row > 9 && row < 54){
        if(col <= 24){
            col = 24;
        }else if(col<row+13 && col<76-row && col>24){
            col = 24;
        }else if(row<30 && col>row+15 && col>101-row){
            row = 9;
        }else if(col>105-row && col>row+42 && col<94){
            col = 94;
        }else if(col >= 94){
            col = 94;
        }else if(row>33 && col<80-row && col<row+38){
            row = 54;
        }else{
            return;
        }
    }else if(row>=54 && row<60){
        if(col<=24){
            row = 54;
            col = 24;
        }else if(col>24 && col<94){
            row = 54;
        }else{
            row = 54;
            col = 94;
        }
    }else{
      return;
    }

    position[0] = row;
    position[1] = col;
}

int update_current_position(uint8_t* position) {
    int distances[4];
    uint8_t original_position[2];

    receive_dwm1000_distances(distances);
    // Debuging
    // printf("%dmm | %dmm | %dmm | %dmm \n",distances[0],distances[1],distances[2],distances[3]);

    trilaterate(distances, original_position);

    correction(original_position, position);

    return 0;
}
