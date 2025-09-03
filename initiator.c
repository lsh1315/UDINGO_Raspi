#include <DWM_functions.h>
#include "main.h"
#include "deca_device_api.h"
#include "deca_regs.h"
#include "deca_timestamps.h"
#include "port.h"
#include <string.h>
#include <stdio.h>

extern UART_HandleTypeDef huart2;

#define RNG_DELAY_MS 650
#define TX_ANT_DLY     16590
#define RX_ANT_DLY     16590
#define ALL_MSG_COMMON_LEN            10
#define ALL_MSG_SN_IDX                2
#define FINAL_MSG_TS_LEN              4
#define FINAL_MSG_POLL_TX_TS_IDX      10
#define FINAL_MSG_RESP_RX_TS_IDX      14
#define FINAL_MSG_FINAL_TX_TS_IDX     18
#define UUS_TO_DWT_TIME   65536
#define SPEED_OF_LIGHT  299792458
#define POLL_TX_TO_RESP_RX_DLY_UUS 5000 //300
#define RESP_RX_TIMEOUT_UUS 50000 //3500
#define RESP_RX_TO_FINAL_TX_DLY_UUS 30000 //3500
#define PRE_TIMEOUT 300 //30
#define RX_BUF_LEN  20

static dwt_config_t config = {
    2, DWT_PRF_64M, DWT_PLEN_1024, DWT_PAC32, 9, 9, 1, DWT_BR_110K,
    DWT_PHRMODE_STD, (1025 + 64 - 32)
};

static uint8_t frame_seq_nb = 0;
char uart_msg[128];

static uint8_t tx_poll_msg[]  = {0x41, 0x88, 0, 0xCA, 0xDE, 'W', 'A', '4', 'E', 0x21, 0, 0};
static uint8_t rx_resp_msg[]  = {0x41, 0x88, 0, 0xCA, 0xDE, 'V', 'E', '4', 'A', 0x10, 0x02, 0, 0, 0, 0};
static uint8_t tx_final_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'W', 'A', '4', 'E', 0x23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

static uint8_t rx_buffer[RX_BUF_LEN];
uint32_t frameLen, final_tx_time;
uint64_t poll_tx_ts, resp_rx_ts, final_tx_ts;
static uint32_t status = 0;

void ds_twr_init(void)
{
    deca_reset();
    port_set_dw1000_slowrate();
    if (dwt_initialise(DWT_LOADUCODE) == DWT_ERROR) while (1) {};
    port_set_dw1000_fastrate();
    dwt_configure(&config);

    dwt_settxantennadelay(TX_ANT_DLY);
    dwt_setrxantennadelay(RX_ANT_DLY);
    dwt_setrxaftertxdelay(POLL_TX_TO_RESP_RX_DLY_UUS);
    dwt_setrxtimeout(RESP_RX_TIMEOUT_UUS);
    dwt_setpreambledetecttimeout(PRE_TIMEOUT);

    while (1)
    {
        sprintf(uart_msg, "[UWB] Sending poll with seq %d\r\n", frame_seq_nb);
        HAL_UART_Transmit(&huart2, (uint8_t*)uart_msg, strlen(uart_msg), 100);

        tx_poll_msg[ALL_MSG_COMMON_LEN] = frame_seq_nb;
        dwt_writetxdata(sizeof(tx_poll_msg), tx_poll_msg, 0);
        dwt_writetxfctrl(sizeof(tx_poll_msg), 0, 1);
        dwt_starttx(DWT_START_TX_IMMEDIATE | DWT_RESPONSE_EXPECTED);

        do {
            status = dwt_read32bitreg(SYS_STATUS_ID);
        } while (!(status & (SYS_STATUS_RXFCG | SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR)));

        frame_seq_nb++;

        if (status & SYS_STATUS_RXFCG)
        {
            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_RXFCG | SYS_STATUS_TXFRS);

            memset(rx_buffer, 0, RX_BUF_LEN);
            frameLen = dwt_read32bitreg(RX_FINFO_ID) & 0x0000007FUL;
            if (frameLen <= RX_BUF_LEN)
                dwt_readrxdata(rx_buffer, frameLen, 0);

            rx_buffer[ALL_MSG_SN_IDX] = 0;
            if (memcmp(rx_buffer, rx_resp_msg, ALL_MSG_COMMON_LEN) == 0)
            {
                poll_tx_ts = get_tx_timestamp_u64();
                resp_rx_ts = get_rx_timestamp_u64();

                sprintf(uart_msg, "[UWB] Response received. T1 = %lu, T4 = %lu\r\n", (uint32_t)poll_tx_ts, (uint32_t)resp_rx_ts);
                HAL_UART_Transmit(&huart2, (uint8_t*)uart_msg, strlen(uart_msg), 100);

                final_tx_time = (resp_rx_ts + (RESP_RX_TO_FINAL_TX_DLY_UUS * UUS_TO_DWT_TIME)) >> 8;
                dwt_setdelayedtrxtime(final_tx_time);
                final_tx_ts = (((uint64_t)(final_tx_time & 0xFFFFFFFEUL)) << 8) + TX_ANT_DLY;

                final_msg_set_ts(&tx_final_msg[FINAL_MSG_POLL_TX_TS_IDX], poll_tx_ts);
                final_msg_set_ts(&tx_final_msg[FINAL_MSG_RESP_RX_TS_IDX], resp_rx_ts);
                final_msg_set_ts(&tx_final_msg[FINAL_MSG_FINAL_TX_TS_IDX], final_tx_ts);

                tx_final_msg[ALL_MSG_SN_IDX] = frame_seq_nb;
                dwt_writetxdata(sizeof(tx_final_msg), tx_final_msg, 0);
                dwt_writetxfctrl(sizeof(tx_final_msg), 0, 1);

                int ret = dwt_starttx(DWT_START_TX_DELAYED);
                if (ret == DWT_SUCCESS)
                {
                    while (!(dwt_read32bitreg(SYS_STATUS_ID) & SYS_STATUS_TXFRS)) {};
                    dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_TXFRS);
                    frame_seq_nb++;

                    sprintf(uart_msg, "[UWB] Final message sent. T5 = %lu\r\n", (uint32_t)final_tx_ts);
                    HAL_UART_Transmit(&huart2, (uint8_t*)uart_msg, strlen(uart_msg), 100);
                }
                else
                {
                    sprintf(uart_msg, "[UWB] Final TX scheduling failed.\r\n");
                    HAL_UART_Transmit(&huart2, (uint8_t*)uart_msg, strlen(uart_msg), 100);
                }
            }
        }
        else
        {
            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR);
            dwt_rxreset();
            sprintf(uart_msg, "[UWB] Response not received or RX error.\r\n");
            HAL_UART_Transmit(&huart2, (uint8_t*)uart_msg, strlen(uart_msg), 100);
        }

        Sleep(RNG_DELAY_MS);
    }
}
