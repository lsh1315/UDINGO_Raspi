///*! ----------------------------------------------------------------------------
// *  @file    main.c
// *  @brief   Single-sided two-way ranging (SS TWR) responder example code
// *
// *           This is a simple code example which acts as the responder in a SS TWR distance measurement exchange. This application waits for a "poll"
// *           message (recording the RX time-stamp of the poll) expected from the "SS TWR initiator" example code (companion to this application), and
// *           then sends a "response" message to complete the exchange. The response message contains all the time-stamps recorded by this application,
// *           including the calculated/predicted TX time-stamp for the response message itself. The companion "SS TWR initiator" example application
// *           works out the time-of-flight over-the-air and, thus, the estimated distance between the two devices.
// *
// * @attention
// *
// * Copyright 2015 (c) Decawave Ltd, Dublin, Ireland.
// *
// * All rights reserved.
// *
// * @author Decawave
// */
//
///*
// * ss_responder.c
// *
// *  Created on: Jan 18, 2021
// *      Author: kostasdeligiorgis
// */
//
//#include <stdio.h>
//#include <string.h>
//
//#include <DWM_functions.h>
//#include "main.h"
//#include "deca_device_api.h"
//#include "deca_regs.h"
////#include "usbd_cdc_if.h"
//
//
///* Default communication configuration. We use here EVK1000's mode 4. See NOTE 1 below. */
//static dwt_config_t config = {
//    2,               /* Channel number. */
//    DWT_PRF_64M,     /* Pulse repetition frequency. */
//    DWT_PLEN_128,    /* Preamble length. Used in TX only. */
//    DWT_PAC8,        /* Preamble acquisition chunk size. Used in RX only. */
//    9,               /* TX preamble code. Used in TX only. */
//    9,               /* RX preamble code. Used in RX only. */
//    0,               /* 0 to use standard SFD, 1 to use non-standard SFD. */
//    DWT_BR_6M8,      /* Data rate. */
//    DWT_PHRMODE_STD, /* PHY header mode. */
//    (128 +1 + 8 - 8)    /* SFD timeout (preamble length + 1 + SFD length - PAC size). Used in RX only. */
//};
//
///* Default antenna delay values for 64 MHz PRF. See NOTE 2 below. */
//#define TX_ANT_DLY 16505
//#define RX_ANT_DLY 16505
//
///* Frames used in the ranging process. See NOTE 3 below. */
//static uint8 rx_poll_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'W', 'A', '1', 'E', 0xE0, 0, 0};
//static uint8 tx_resp_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'V', 'E', '1', 'A', 0xE1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
//
///* Length of the common part of the message (up to and including the function code, see NOTE 3 below). */
//#define ALL_MSG_COMMON_LEN 10
///* Index to access some of the fields in the frames involved in the process. */
//#define ALL_MSG_SN_IDX 2
//#define RESP_MSG_POLL_RX_TS_IDX 10
//#define RESP_MSG_RESP_TX_TS_IDX 14
//#define RESP_MSG_TS_LEN 4
///* Frame sequence number, incremented after each transmission. */
//static uint8 frame_seq_nb = 0;
//
///* Buffer to store received messages.
// * Its size is adjusted to longest frame that this example code is supposed to handle. */
//#define RX_BUF_LEN 12
//static uint8 rx_buffer[RX_BUF_LEN];
//
///* Hold copy of status register state here for reference so that it can be examined at a debug breakpoint. */
//static uint32 status_reg = 0;
//
///* UWB microsecond (uus) to device time unit (dtu, around 15.65 ps) conversion factor.
// * 1 uus = 512 / 499.2 Βs and 1 Βs = 499.2 * 128 dtu. */
//#define UUS_TO_DWT_TIME 65536
//
///* Delay between frames, in UWB microseconds. See NOTE 1 below. */
////#define POLL_RX_TO_RESP_TX_DLY_UUS 330
//#define POLL_RX_TO_RESP_TX_DLY_UUS 5000 // it works
////#define POLL_RX_TO_RESP_TX_DLY_UUS 850  // it works
////#define POLL_RX_TO_RESP_TX_DLY_UUS 715
//
//
///* Timestamps of frames transmission/reception.
// * As they are 40-bit wide, we need to define a 64-bit int type to handle them. */
//typedef unsigned long long uint64;
//static uint64 poll_rx_ts;
//static uint64 resp_tx_ts;
//
///* Declaration of static functions. */
//static uint64 get_rx_timestamp_u64(void);
//static void resp_msg_set_ts(uint8 *ts_field, const uint64 ts);
//
//extern UART_HandleTypeDef huart2;
//
///*! ------------------------------------------------------------------------------------------------------------------
// * @fn main()
// *
// * @brief Application entry point.
// *
// * @param  none
// *
// * @return none
// */
//int ss_resp_main(void)
//{
//    deca_reset();
//    port_set_dw1000_slowrate();
//
//    HAL_UART_Transmit(&huart2, (uint8_t *)"DW1000 Reset Done\r\n", 21, 100);
//
//    if (dwt_initialise(DWT_LOADUCODE) == DWT_ERROR)
//    {
//        HAL_UART_Transmit(&huart2, (uint8_t *)"DW1000 Init FAILED\r\n", 22, 100);
//        while (1);
//    }
//
//    port_set_dw1000_fastrate();
//    HAL_UART_Transmit(&huart2, (uint8_t *)"DW1000 Init OK\r\n", 17, 100);
//
//    dwt_configure(&config);
//    dwt_setrxantennadelay(RX_ANT_DLY);
//    dwt_settxantennadelay(TX_ANT_DLY);
//
//    while (1)
//    {
//        HAL_UART_Transmit(&huart2, (uint8_t *)"Waiting for Poll frame...\r\n", 28, 100);
//        dwt_rxenable(DWT_START_RX_IMMEDIATE);
//
//        while (!((status_reg = dwt_read32bitreg(SYS_STATUS_ID)) &
//                (SYS_STATUS_RXFCG | SYS_STATUS_ALL_RX_ERR)))
//        {
//            // 대기 중
//        }
//
//        if (status_reg & SYS_STATUS_RXFCG)
//        {
//            HAL_UART_Transmit(&huart2, (uint8_t *)"Poll frame received\r\n", 22, 100);
//
//            uint32 frame_len;
//            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_RXFCG);
//
//            frame_len = dwt_read32bitreg(RX_FINFO_ID) & RX_FINFO_RXFL_MASK_1023;
//            if (frame_len <= RX_BUF_LEN)
//            {
//                dwt_readrxdata(rx_buffer, frame_len, 0);
//            }
//
//            rx_buffer[ALL_MSG_SN_IDX] = 0;
//
//            if (memcmp(rx_buffer, rx_poll_msg, ALL_MSG_COMMON_LEN) == 0)
//            {
//                uint32 resp_tx_time;
//                int ret;
//
//                poll_rx_ts = get_rx_timestamp_u64();
//                resp_tx_time = (poll_rx_ts + (POLL_RX_TO_RESP_TX_DLY_UUS * UUS_TO_DWT_TIME)) >> 8;
//                dwt_setdelayedtrxtime(resp_tx_time);
//
//                resp_tx_ts = (((uint64)(resp_tx_time & 0xFFFFFFFEUL)) << 8) + TX_ANT_DLY;
//                resp_msg_set_ts(&tx_resp_msg[RESP_MSG_POLL_RX_TS_IDX], poll_rx_ts);
//                resp_msg_set_ts(&tx_resp_msg[RESP_MSG_RESP_TX_TS_IDX], resp_tx_ts);
//
//                tx_resp_msg[ALL_MSG_SN_IDX] = frame_seq_nb;
//                dwt_writetxdata(sizeof(tx_resp_msg), tx_resp_msg, 0);
//                dwt_writetxfctrl(sizeof(tx_resp_msg), 0, 1);
//                ret = dwt_starttx(DWT_START_TX_DELAYED);
//
//                if (ret == DWT_ERROR)
//                {
//                    HAL_UART_Transmit(&huart2, (uint8_t *)"TX Delayed Failed\r\n", 20, 100);
//                    continue; // 다음 루프로
//                }
//
//                HAL_UART_Transmit(&huart2, (uint8_t *)"Sending Response...\r\n", 22, 100);
//
//                while (!(dwt_read32bitreg(SYS_STATUS_ID) & SYS_STATUS_TXFRS))
//                {
//                    // TX 완료 대기
//                }
//
//                //HAL_UART_Transmit(&huart2, (uint8_t *)"Tx Complete\r\n", 20, 100);
//
//                dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_TXFRS);
//                frame_seq_nb++;
//            }
//            else
//            {
//                HAL_UART_Transmit(&huart2, (uint8_t *)"Invalid Poll frame\r\n", 21, 100);
//            }
//        }
//        else
//        {
//            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_ALL_RX_ERR);
//            dwt_rxreset();
//            uint32_t err_status = dwt_read32bitreg(SYS_STATUS_ID);
//            char msg[64];
//            sprintf(msg, "RX Error status: 0x%08lX\r\n", err_status);
//            HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
//
//        }
//    }
//}
//
//
///*! ------------------------------------------------------------------------------------------------------------------
// * @fn get_rx_timestamp_u64()
// *
// * @brief Get the RX time-stamp in a 64-bit variable.
// *        /!\ This function assumes that length of time-stamps is 40 bits, for both TX and RX!
// *
// * @param  none
// *
// * @return  64-bit value of the read time-stamp.
// */
//static uint64 get_rx_timestamp_u64(void)
//{
//    uint8 ts_tab[5];
//    uint64 ts = 0;
//    int i;
//    dwt_readrxtimestamp(ts_tab);
//    for (i = 4; i >= 0; i--)
//    {
//        ts <<= 8;
//        ts |= ts_tab[i];
//    }
//    return ts;
//}
//
///*! ------------------------------------------------------------------------------------------------------------------
// * @fn final_msg_set_ts()
// *
// * @brief Fill a given timestamp field in the response message with the given value. In the timestamp fields of the
// *        response message, the least significant byte is at the lower address.
// *
// * @param  ts_field  pointer on the first byte of the timestamp field to fill
// *         ts  timestamp value
// *
// * @return none
// */
//static void resp_msg_set_ts(uint8 *ts_field, const uint64 ts)
//{
//    int i;
//    for (i = 0; i < RESP_MSG_TS_LEN; i++)
//    {
//        ts_field[i] = (ts >> (i * 8)) & 0xFF;
//    }
//}
//
///*****************************************************************************************************************************************************
// * NOTES:
// *
// * 1. The single-sided two-way ranging scheme implemented here has to be considered carefully as the accuracy of the distance measured is highly
// *    sensitive to the clock offset error between the devices and the length of the response delay between frames. To achieve the best possible
// *    accuracy, this response delay must be kept as low as possible. In order to do so, 6.8 Mbps data rate is used in this example and the response
// *    delay between frames is defined as low as possible. The user is referred to User Manual for more details about the single-sided two-way ranging
// *    process.
// * 2. The sum of the values is the TX to RX antenna delay, experimentally determined by a calibration process. Here we use a hard coded typical value
// *    but, in a real application, each device should have its own antenna delay properly calibrated to get the best possible precision when performing
// *    range measurements.
// * 3. The frames used here are Decawave specific ranging frames, complying with the IEEE 802.15.4 standard data frame encoding. The frames are the
// *    following:
// *     - a poll message sent by the initiator to trigger the ranging exchange.
// *     - a response message sent by the responder to complete the exchange and provide all information needed by the initiator to compute the
// *       time-of-flight (distance) estimate.
// *    The first 10 bytes of those frame are common and are composed of the following fields:
// *     - byte 0/1: frame control (0x8841 to indicate a data frame using 16-bit addressing).
// *     - byte 2: sequence number, incremented for each new frame.
// *     - byte 3/4: PAN ID (0xDECA).
// *     - byte 5/6: destination address, see NOTE 4 below.
// *     - byte 7/8: source address, see NOTE 4 below.
// *     - byte 9: function code (specific values to indicate which message it is in the ranging process).
// *    The remaining bytes are specific to each message as follows:
// *    Poll message:
// *     - no more data
// *    Response message:
// *     - byte 10 -> 13: poll message reception timestamp.
// *     - byte 14 -> 17: response message transmission timestamp.
// *    All messages end with a 2-byte checksum automatically set by DW1000.
// * 4. Source and destination addresses are hard coded constants in this example to keep it simple but for a real product every device should have a
// *    unique ID. Here, 16-bit addressing is used to keep the messages as short as possible but, in an actual application, this should be done only
// *    after an exchange of specific messages used to define those short addresses for each device participating to the ranging exchange.
// * 5. In a real application, for optimum performance within regulatory limits, it may be necessary to set TX pulse bandwidth and TX power, (using
// *    the dwt_configuretxrf API call) to per device calibrated values saved in the target system or the DW1000 OTP memory.
// * 6. We use polled mode of operation here to keep the example as simple as possible but all status events can be used to generate interrupts. Please
// *    refer to DW1000 User Manual for more details on "interrupts". It is also to be noted that STATUS register is 5 bytes long but, as the event we
// *    use are all in the first bytes of the register, we can use the simple dwt_read32bitreg() API call to access it instead of reading the whole 5
// *    bytes.
// * 7. As we want to send final TX timestamp in the final message, we have to compute it in advance instead of relying on the reading of DW1000
// *    register. Timestamps and delayed transmission time are both expressed in device time units so we just have to add the desired response delay to
// *    response RX timestamp to get final transmission time. The delayed transmission time resolution is 512 device time units which means that the
// *    lower 9 bits of the obtained value must be zeroed. This also allows to encode the 40-bit value in a 32-bit words by shifting the all-zero lower
// *    8 bits.
// * 8. In this operation, the high order byte of each 40-bit timestamps is discarded. This is acceptable as those time-stamps are not separated by
// *    more than 2**32 device time units (which is around 67 ms) which means that the calculation of the round-trip delays (needed in the
// *    time-of-flight computation) can be handled by a 32-bit subtraction.
// * 9. dwt_writetxdata() takes the full size of the message as a parameter but only copies (size - 2) bytes as the check-sum at the end of the frame is
// *    automatically appended by the DW1000. This means that our variable could be two bytes shorter without losing any data (but the sizeof would not
// *    work anymore then as we would still have to indicate the full length of the frame to dwt_writetxdata()).
// * 10. When running this example on the EVB1000 platform with the POLL_RX_TO_RESP_TX_DLY response delay provided, the dwt_starttx() is always
// *     successful. However, in cases where the delay is too short (or something else interrupts the code flow), then the dwt_starttx() might be issued
// *     too late for the configured start time. The code below provides an example of how to handle this condition: In this case it abandons the
// *     ranging exchange and simply goes back to awaiting another poll message. If this error handling code was not here, a late dwt_starttx() would
// *     result in the code flow getting stuck waiting subsequent RX event that will will never come. The companion "initiator" example (ex_06a) should
// *     timeout from awaiting the "response" and proceed to send another poll in due course to initiate another ranging exchange.
// * 11. The user is referred to DecaRanging ARM application (distributed with EVK1000 product) for additional practical example of usage, and to the
// *     DW1000 API Guide for more details on the DW1000 driver functions.
// ****************************************************************************************************************************************************/
