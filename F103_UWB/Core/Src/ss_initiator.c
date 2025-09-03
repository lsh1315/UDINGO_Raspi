///*! ----------------------------------------------------------------------------
// *  @file    main.c
// *  @brief   Single-sided two-way ranging (SS TWR) initiator example code
// *
// *           This is a simple code example which acts as the initiator in a SS TWR distance measurement exchange. This application sends a "poll"
// *           frame (recording the TX time-stamp of the poll), after which it waits for a "response" message from the "DS TWR responder" example
// *           code (companion to this application) to complete the exchange. The response message contains the remote responder's time-stamps of poll
// *           RX, and response TX. With this data and the local time-stamps, (of poll TX and response RX), this example application works out a value
// *           for the time-of-flight over-the-air and, thus, the estimated distance between the two devices, which it writes to the LCD.
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
// * ss_initiator.c
// *
// *  Created on: Jan 18, 2021
// *      Author: kostasdeligiorgis
// */
//
//#include <stdio.h>
//#include <string.h>
//
//#include "deca_device_api.h"
//#include "deca_regs.h"
//#include "stdio.h"
//#include <DWM_functions.h>
//#include "main.h"
//
////#include "usbd_cdc_if.h"
//
///* Inter-ranging delay period, in milliseconds. */
////#define RNG_DELAY_MS 1000
//#define RNG_DELAY_MS 850
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
//
///* Length of the common part of the message (up to and including the function code, see NOTE 3 below). */
//#define ALL_MSG_COMMON_LEN 10
///* Indexes to access some of the fields in the frames defined above. */
//#define ALL_MSG_SN_IDX 2
//#define RESP_MSG_POLL_RX_TS_IDX 10
//#define RESP_MSG_RESP_TX_TS_IDX 14
//#define RESP_MSG_TS_LEN 4
///* Frame sequence number, incremented after each transmission. */
//static uint8 frame_seq_nb = 0;
//
///* Buffer to store received response message.
// * Its size is adjusted to longest frame that this example code is supposed to handle. */
//#define RX_BUF_LEN 20
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
//#define POLL_TX_TO_RESP_RX_DLY_UUS 1000 //140
//
///* Receive response timeout. See NOTE 5 below. */
////#define RESP_RX_TIMEOUT_UUS 210
//#define RESP_RX_TIMEOUT_UUS 5000 //600  // it works good 08/03
//
///* Speed of light in air, in meters per second. */
//#define SPEED_OF_LIGHT 299792458
//
///* Hold copies of computed time of flight and distance here for reference so that it can be examined at a debug breakpoint. */
//static double tof;
//static double distance;
//
//extern UART_HandleTypeDef huart2;
//
//uint8_t dist[30];
//
//uint8_t table[] = {'1','2','3'};
//
///* Declaration of static functions. */
//static void resp_msg_get_ts(uint8 *ts_field, uint32 *ts);
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
//
//int ss_init_main(int x)
//{
//    /* Frames used in the ranging process. See NOTE 3 below. */
//    uint8 tx_poll_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'W', 'A', table[x], 'E', 0xE0, 0, 0};
//    uint8 rx_resp_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'V', 'E', table[x], 'A', 0xE1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
//
//    deca_reset();
//    port_set_dw1000_slowrate();
//
//    HAL_UART_Transmit(&huart2, (uint8_t *)"DW1000 Reset Done\r\n", 20, 100);
//
//    uint32_t devid = dwt_readdevid();
//    char msg[64];
//    sprintf(msg, "DEVID: 0x%08lX\r\n", devid);
//    HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
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
//    dwt_setrxaftertxdelay(POLL_TX_TO_RESP_RX_DLY_UUS);
//    dwt_setrxtimeout(RESP_RX_TIMEOUT_UUS);
//
//    while (1)
//    {
//        HAL_UART_Transmit(&huart2, (uint8_t *)"Sending Poll Frame\r\n", 21, 100);
//
//        tx_poll_msg[ALL_MSG_SN_IDX] = frame_seq_nb;
//        dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_TXFRS);
//        dwt_writetxdata(sizeof(tx_poll_msg), tx_poll_msg, 0);
//        dwt_writetxfctrl(sizeof(tx_poll_msg), 0, 1);
//        dwt_starttx(DWT_START_TX_IMMEDIATE | DWT_RESPONSE_EXPECTED);
//
//        HAL_UART_Transmit(&huart2, (uint8_t *)"Waiting for Response\r\n", 23, 100);
//
//        while (!((status_reg = dwt_read32bitreg(SYS_STATUS_ID)) &
//                (SYS_STATUS_RXFCG | SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR)))
//        {
//            // Optional: Insert delay here if needed
//        }
//
//        frame_seq_nb++;
//
//        if (status_reg & SYS_STATUS_RXFCG)
//        {
//            HAL_UART_Transmit(&huart2, (uint8_t *)"Response Frame Received\r\n", 26, 100);
//
//            uint32 frame_len;
//            dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_RXFCG);
//            frame_len = dwt_read32bitreg(RX_FINFO_ID) & RX_FINFO_RXFLEN_MASK;
//
//            if (frame_len <= RX_BUF_LEN)
//            {
//                dwt_readrxdata(rx_buffer, frame_len, 0);
//            }
//
//            rx_buffer[ALL_MSG_SN_IDX] = 0;
//            if (memcmp(rx_buffer, rx_resp_msg, ALL_MSG_COMMON_LEN) == 0)
//            {
//                uint32 poll_tx_ts, resp_rx_ts, poll_rx_ts, resp_tx_ts;
//                int32 rtd_init, rtd_resp;
//                float clockOffsetRatio;
//
//                poll_tx_ts = dwt_readtxtimestamplo32();
//                resp_rx_ts = dwt_readrxtimestamplo32();
//                clockOffsetRatio = dwt_readcarrierintegrator() * (FREQ_OFFSET_MULTIPLIER * HERTZ_TO_PPM_MULTIPLIER_CHAN_2 / 1.0e6);
//
//                resp_msg_get_ts(&rx_buffer[RESP_MSG_POLL_RX_TS_IDX], &poll_rx_ts);
//                resp_msg_get_ts(&rx_buffer[RESP_MSG_RESP_TX_TS_IDX], &resp_tx_ts);
//
//                rtd_init = resp_rx_ts - poll_tx_ts;
//                rtd_resp = resp_tx_ts - poll_rx_ts;
//
//                tof = ((rtd_init - rtd_resp * (1 - clockOffsetRatio)) / 2.0) * DWT_TIME_UNITS;
//                distance = tof * SPEED_OF_LIGHT;
//
//                sprintf(msg, "Distance calculated: %.2lf m\r\n", distance);
//                HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
//            }
//            else
//            {
//                HAL_UART_Transmit(&huart2, (uint8_t *)"Invalid Response Frame\r\n", 25, 100);
//            }
//        }
//        else
//        {
//             HAL_UART_Transmit(&huart2, (uint8_t *)"RX Timeout or Error\r\n", 22, 100);
//
//             // 디버깅: status_reg 출력
//             sprintf(msg, "Status Reg: 0x%08lX\r\n", status_reg);
//             HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
//
//             uint16 rssi = dwt_read16bitoffsetreg(RX_FQUAL_ID, 0x0C);  // example
//             sprintf(msg, "RSSI: %u\r\n", rssi);
//             HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
//
//             // 오류 초기화 및 리셋
//             dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR);
//             dwt_rxreset();
//        }
//
//        Sleep(RNG_DELAY_MS);
//    }
//}
//
//
///*! ------------------------------------------------------------------------------------------------------------------
// * @fn resp_msg_get_ts()
// *
// * @brief Read a given timestamp value from the response message. In the timestamp fields of the response message, the
// *        least significant byte is at the lower address.
// *
// * @param  ts_field  pointer on the first byte of the timestamp field to get
// *         ts  timestamp value
// *
// * @return none
// */
//static void resp_msg_get_ts(uint8 *ts_field, uint32 *ts)
//{
//    int i;
//    *ts = 0;
//    for (i = 0; i < RESP_MSG_TS_LEN; i++)
//    {
//        *ts += ts_field[i] << (i * 8);
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
// *    process.  NB:SEE ALSO NOTE 11.
// * 2. The sum of the values is the TX to RX antenna delay, this should be experimentally determined by a calibration process. Here we use a hard coded
// *    value (expected to be a little low so a positive error will be seen on the resultant distance estimate. For a real production application, each
// *    device should have its own antenna delay properly calibrated to get good precision when performing range measurements.
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
// * 5. This timeout is for complete reception of a frame, i.e. timeout duration must take into account the length of the expected frame. Here the value
// *    is arbitrary but chosen large enough to make sure that there is enough time to receive the complete response frame sent by the responder at the
// *    6.8M data rate used (around 200 Βs).
// * 6. In a real application, for optimum performance within regulatory limits, it may be necessary to set TX pulse bandwidth and TX power, (using
// *    the dwt_configuretxrf API call) to per device calibrated values saved in the target system or the DW1000 OTP memory.
// * 7. dwt_writetxdata() takes the full size of the message as a parameter but only copies (size - 2) bytes as the check-sum at the end of the frame is
// *    automatically appended by the DW1000. This means that our variable could be two bytes shorter without losing any data (but the sizeof would not
// *    work anymore then as we would still have to indicate the full length of the frame to dwt_writetxdata()).
// * 8. We use polled mode of operation here to keep the example as simple as possible but all status events can be used to generate interrupts. Please
// *    refer to DW1000 User Manual for more details on "interrupts". It is also to be noted that STATUS register is 5 bytes long but, as the event we
// *    use are all in the first bytes of the register, we can use the simple dwt_read32bitreg() API call to access it instead of reading the whole 5
// *    bytes.
// * 9. The high order byte of each 40-bit time-stamps is discarded here. This is acceptable as, on each device, those time-stamps are not separated by
// *    more than 2**32 device time units (which is around 67 ms) which means that the calculation of the round-trip delays can be handled by a 32-bit
// *    subtraction.
// * 10. The user is referred to DecaRanging ARM application (distributed with EVK1000 product) for additional practical example of usage, and to the
// *     DW1000 API Guide for more details on the DW1000 driver functions.
// * 11. The use of the carrier integrator value to correct the TOF calculation, was added Feb 2017 for v1.3 of this example.  This significantly
// *     improves the result of the SS-TWR where the remote responder unit's clock is a number of PPM offset from the local inmitiator unit's clock.
// *     As stated in NOTE 2 a fixed offset in range will be seen unless the antenna delsy is calibratred and set correctly.
// *
// ****************************************************************************************************************************************************/
