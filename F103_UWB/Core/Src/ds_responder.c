#include <stdio.h>
#include <string.h>
#include <math.h>

#include <DWM_functions.h>
#include "main.h"
#include "deca_device_api.h"
#include "deca_regs.h"
#include "deca_timestamps.h"
#include "port.h"

extern UART_HandleTypeDef huart2;

#define TX_ANT_DLY 16505
#define RX_ANT_DLY 16505

#define ALL_MSG_COMMON_LEN            10
#define ALL_MSG_SN_IDX                2
#define FINAL_MSG_TS_LEN              4
#define FINAL_MSG_POLL_TX_TS_IDX      10
#define FINAL_MSG_RESP_RX_TS_IDX      14
#define FINAL_MSG_FINAL_TX_TS_IDX     18

#define UUS_TO_DWT_TIME    65536
#define SPEED_OF_LIGHT     299792458

static dwt_config_t config = {
    2, DWT_PRF_64M, DWT_PLEN_1024, DWT_PAC32, 9, 9, 1, DWT_BR_110K,
    DWT_PHRMODE_STD, (1024 + 1 + 64 - 32)
};

#define POLL_RX_TO_RESP_TX_DLY_UUS 10000 //fix
#define RESP_TX_TO_FINAL_RX_DLY_UUS 20000 //500
#define FINAL_RX_TIMEOUT_UUS 60000 //5000
#define PRE_TIMEOUT 500

typedef signed long long int64;
typedef unsigned long long uint64;

static uint8_t frame_seq_nb = 0;
char msg[128];

#define RX_RESP_BUF_LEN  24
static uint8_t rx_resp_buffer[RX_RESP_BUF_LEN];

static uint64 poll_rx_ts, resp_tx_ts, final_rx_ts;
double tof, distance;

uint8_t table[] = {'1','2','3','4'};

void ds_resp_main(int x, int* dist)
{
    uint32_t frameLen, resp_tx_time;
    uint32_t status = 0;

    deca_reset();
    port_set_dw1000_slowrate();
    if (dwt_initialise(DWT_LOADUCODE) == DWT_ERROR) while (1) {};
    port_set_dw1000_fastrate();
    dwt_configure(&config);

    dwt_setrxantennadelay(RX_ANT_DLY);
    dwt_settxantennadelay(TX_ANT_DLY);
    dwt_setpreambledetecttimeout(PRE_TIMEOUT);

    uint8_t rx_poll_msg[]  = {0x41, 0x88, 0, 0xCA, 0xDE, 'W','A',table[x],'E', 0x21, 0, 0};
    uint8_t tx_resp_msg[]  = {0x41, 0x88, 0, 0xCA, 0xDE, 'V','E',table[x],'A', 0x10, 0x02, 0, 0, 0, 0};
    uint8_t rx_final_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'W','A',table[x],'E', 0x23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    while(1){
        dwt_setrxtimeout(0);
        dwt_rxenable(DWT_START_RX_IMMEDIATE);

        do {
            status = dwt_read32bitreg(SYS_STATUS_ID);
        } while (!(status & (SYS_STATUS_RXFCG | SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR)));

        if (status & SYS_STATUS_RXFCG)
        {
            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_RXFCG);
            memset(rx_resp_buffer, 0, RX_RESP_BUF_LEN);
            frameLen = dwt_read32bitreg(RX_FINFO_ID) & RX_FINFO_RXFL_MASK_1023;
            if (frameLen <= RX_RESP_BUF_LEN)
                dwt_readrxdata(rx_resp_buffer, frameLen, 0);

            rx_resp_buffer[ALL_MSG_SN_IDX] = 0;
            if (memcmp(rx_resp_buffer, rx_poll_msg, ALL_MSG_COMMON_LEN) == 0)
            {
                poll_rx_ts = get_rx_timestamp_u64();
                sprintf(msg, "[UWB] Poll received, T2 = %lu\r\n", (uint32_t)poll_rx_ts);
                //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

                resp_tx_time = (poll_rx_ts + (POLL_RX_TO_RESP_TX_DLY_UUS * UUS_TO_DWT_TIME)) >> 8;
                dwt_setdelayedtrxtime(resp_tx_time);

                dwt_setrxaftertxdelay(RESP_TX_TO_FINAL_RX_DLY_UUS);
                dwt_setrxtimeout(FINAL_RX_TIMEOUT_UUS);

                tx_resp_msg[ALL_MSG_SN_IDX] = frame_seq_nb;
                dwt_writetxdata(sizeof(tx_resp_msg), tx_resp_msg, 0);
                dwt_writetxfctrl(sizeof(tx_resp_msg), 0, 1);
                int ret = dwt_starttx(DWT_START_TX_DELAYED | DWT_RESPONSE_EXPECTED);

                if (ret == DWT_ERROR) {
                    sprintf(msg, "[UWB] Response TX scheduling failed.\r\n");
                    //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
                    return;
                } else {
                    sprintf(msg, "[UWB] Response scheduled, T3 approx = %lu\r\n", (uint32_t)(resp_tx_time << 8));
                    //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
                }

                do {
                    status = dwt_read32bitreg(SYS_STATUS_ID);
                } while (!(status & (SYS_STATUS_RXFCG | SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR)));

                frame_seq_nb++;

                if (status & SYS_STATUS_RXFCG)
                {
                    dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_RXFCG | SYS_STATUS_TXFRS);
                    memset(rx_resp_buffer, 0, RX_RESP_BUF_LEN);
                    frameLen = dwt_read32bitreg(RX_FINFO_ID) & RX_FINFO_RXFLEN_MASK;
                    if (frameLen <= RX_RESP_BUF_LEN)
                        dwt_readrxdata(rx_resp_buffer, frameLen, 0);

                    rx_resp_buffer[ALL_MSG_SN_IDX] = 0;
                    if (memcmp(rx_resp_buffer, rx_final_msg, ALL_MSG_COMMON_LEN) == 0)
                    {
                        uint32_t poll_tx_ts, resp_rx_ts, final_tx_ts;
                        uint32_t poll_rx_ts_32, resp_tx_ts_32, final_rx_ts_32;
                        double Ra, Rb, Da, Db;
                        int64 tof_dtu;

                        resp_tx_ts  = get_tx_timestamp_u64();
                        final_rx_ts = get_rx_timestamp_u64();

                        sprintf(msg, "[UWB] Final received, T6 = %lu\r\n", (uint32_t)final_rx_ts);
                        //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

                        final_msg_get_ts(&rx_resp_buffer[FINAL_MSG_POLL_TX_TS_IDX],  &poll_tx_ts);
                        final_msg_get_ts(&rx_resp_buffer[FINAL_MSG_RESP_RX_TS_IDX],  &resp_rx_ts);
                        final_msg_get_ts(&rx_resp_buffer[FINAL_MSG_FINAL_TX_TS_IDX], &final_tx_ts);

                        sprintf(msg, "[UWB] Final contained T1=%lu, T4=%lu, T5=%lu\r\n", poll_tx_ts, resp_rx_ts, final_tx_ts);
                        //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

                        poll_rx_ts_32 = (uint32_t)poll_rx_ts;
                        resp_tx_ts_32 = (uint32_t)resp_tx_ts;
                        final_rx_ts_32 = (uint32_t)final_rx_ts;
                        Ra = (double)(resp_rx_ts - poll_tx_ts);
                        Rb = (double)(final_rx_ts_32 - resp_tx_ts_32);
                        Da = (double)(final_tx_ts - resp_rx_ts);
                        Db = (double)(resp_tx_ts_32 - poll_rx_ts_32);
                        tof_dtu = (int64)((Ra * Rb - Da * Db) / (Ra + Rb + Da + Db));

                        sprintf(msg, "%.2lf / %.2lf / %.2lf / %.2lf \r\n", Ra, Rb, Da, Db);
                        //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

                        tof = tof_dtu * DWT_TIME_UNITS;
                        distance = tof * SPEED_OF_LIGHT+1.2;

                        sprintf(msg, "Distance calculated: %.2lf m\r\n", distance);
                        //HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

                        *dist = (int)round(1000*distance);
                        break;
                    }
                }
                else {
                    dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR);
                    dwt_rxreset();
                }
            }
        }
        else {
            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR);
            dwt_rxreset();
        }
    }
}
