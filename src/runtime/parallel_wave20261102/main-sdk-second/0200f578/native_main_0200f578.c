#include "context_00.h"
void native_main_0200f578 (PXIFifoTag tag, u32 data, BOOL err)
{
    RTCResult result;
    RTCPxiResult pxiresult;
    u8 command;
    RTCCallback cb;
    if (err) {
        if (native_data_main_020e5438.field_000c.index) {
            native_data_main_020e5438.field_000c.index = 0;
        }
        if (native_data_main_020e5438.field_000c.lock != RTC_LOCK_OFF) {
            native_data_main_020e5438.field_000c.lock = RTC_LOCK_OFF;
        }
        if (native_data_main_020e5438.field_000c.callback) {
            cb = native_data_main_020e5438.field_000c.callback;
            native_data_main_020e5438.field_000c.callback = ((void *)0) ;
            cb(RTC_RESULT_FATAL_ERROR, native_data_main_020e5438.field_000c.callbackArg);
        }
        return;
    }
    command = (u8)((data & 0x00007f00 ) >> 8 );
    pxiresult = (RTCPxiResult)((data & 0x000000ff ) >> 0 );
    if (command == 0x30 ) {
        if (native_data_main_020e5438.field_000c.interrupt) {
            native_data_main_020e5438.field_000c.interrupt();
        }
        return;
    }
    if (pxiresult == RTC_PXI_RESULT_SUCCESS) {
        result = RTC_RESULT_SUCCESS;
        switch (native_data_main_020e5438.field_000c.sequence) {
        case RTC_SEQ_GET_DATE:
        {
            RTCDate * pDst = (RTCDate *)(native_data_main_020e5438.field_000c.buffer[0]);
            RTCRawDate * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->t.date);
            pDst->year = native_fn_0200fac8(pSrc->year);
            pDst->month = native_fn_0200fac8(pSrc->month);
            pDst->day = native_fn_0200fac8(pSrc->day);
            pDst->week = native_fn_0200fedc(pDst);
        }
        break;
        case RTC_SEQ_GET_TIME:
        {
            RTCTime * pDst = (RTCTime *)(native_data_main_020e5438.field_000c.buffer[0]);
            RTCRawTime * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->t.time);
            pDst->hour = native_fn_0200fac8(pSrc->hour);
            pDst->minute = native_fn_0200fac8(pSrc->minute);
            pDst->second = native_fn_0200fac8(pSrc->second);
        }
        break;
        case RTC_SEQ_GET_DATETIME:
        {
            RTCDate * pDst = (RTCDate *)(native_data_main_020e5438.field_000c.buffer[0]);
            RTCRawDate * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->t.date);
            pDst->year = native_fn_0200fac8(*(u32 *)pSrc & 0x000000ff);
            pDst->month = native_fn_0200fac8(pSrc->month);
            pDst->day = native_fn_0200fac8(pSrc->day);
            pDst->week = native_fn_0200fedc(pDst);
        }
            {
                RTCTime * pDst = (RTCTime *)(native_data_main_020e5438.field_000c.buffer[1]);
                RTCRawTime * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->t.time);
                pDst->hour = native_fn_0200fac8(pSrc->hour);
                pDst->minute = native_fn_0200fac8(pSrc->minute);
                pDst->second = native_fn_0200fac8(pSrc->second);
            }
            break;
        case RTC_SEQ_SET_DATE:
        case RTC_SEQ_SET_TIME:
        case RTC_SEQ_SET_DATETIME:
            break;
        case RTC_SEQ_GET_ALARM1_STATUS:
        {
            RTCAlarmStatus * pDst = (RTCAlarmStatus *)(native_data_main_020e5438.field_000c.buffer[0]);
            RTCRawStatus2 * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->a.status2);
            switch (pSrc->intr_mode) {
            case 0x4 :
                *pDst = RTC_ALARM_STATUS_ON;
                break;
            default:
                *pDst = RTC_ALARM_STATUS_OFF;
            }
        }
        break;
        case RTC_SEQ_GET_ALARM2_STATUS:
        {
            RTCAlarmStatus * pDst = (RTCAlarmStatus *)(native_data_main_020e5438.field_000c.buffer[0]);
            RTCRawStatus2 * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->a.status2);
            if (pSrc->intr2_mode) {
                *pDst = RTC_ALARM_STATUS_ON;
            } else {
                *pDst = RTC_ALARM_STATUS_OFF;
            }
        }
        break;
        case RTC_SEQ_GET_ALARM_PARAM:
        {
            RTCAlarmParam * pDst = (RTCAlarmParam *)(native_data_main_020e5438.field_000c.buffer[0]);
            RTCRawAlarm * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->a.alarm);
            pDst->week = (RTCWeek)(pSrc->week);
            pDst->hour = native_fn_0200fac8(pSrc->hour);
            pDst->minute = native_fn_0200fac8(pSrc->minute);
            pDst->enable = 0x0000 ;
            if (pSrc->we)
                pDst->enable += 0x0001 ;
            if (pSrc->he)
                pDst->enable += 0x0002 ;
            if (pSrc->me)
                pDst->enable += 0x0004 ;
        }
        break;
        case RTC_SEQ_SET_ALARM1_STATUS:
            if (native_data_main_020e5438.field_000c.index == 0) {
                RTCRawStatus2 * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->a.status2);
                if (*(RTCAlarmStatus *)(native_data_main_020e5438.field_000c.buffer[0]) == RTC_ALARM_STATUS_ON) {
                    if (pSrc->intr_mode != 0x4 ) {
                        native_data_main_020e5438.field_000c.index++;
                        pSrc->intr_mode = 0x4 ;
                        if (!native_fn_0200fb90()) {
                            native_data_main_020e5438.field_000c.index = 0;
                            result = RTC_RESULT_SEND_ERROR;
                        }
                    }
                } else {
                    if (pSrc->intr_mode != 0x0 ) {
                        native_data_main_020e5438.field_000c.index++;
                        pSrc->intr_mode = 0x0 ;
                        if (!native_fn_0200fb90()) {
                            native_data_main_020e5438.field_000c.index = 0;
                            result = RTC_RESULT_SEND_ERROR;
                        }
                    }
                }
            } else {
                native_data_main_020e5438.field_000c.index = 0;
            }
            break;
        case RTC_SEQ_SET_ALARM2_STATUS:
            if (native_data_main_020e5438.field_000c.index == 0) {
                RTCRawStatus2 * pSrc = &(((RTCRawData *)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->real_time_clock))->a.status2);
                if (*(RTCAlarmStatus *)(native_data_main_020e5438.field_000c.buffer[0]) == RTC_ALARM_STATUS_ON) {
                    if (!pSrc->intr2_mode) {
                        native_data_main_020e5438.field_000c.index++;
                        pSrc->intr2_mode = 1;
                        if (!native_fn_0200fb90()) {
                            native_data_main_020e5438.field_000c.index = 0;
                            result = RTC_RESULT_SEND_ERROR;
                        }
                    }
                } else {
                    if (pSrc->intr2_mode) {
                        native_data_main_020e5438.field_000c.index++;
                        pSrc->intr2_mode = 0;
                        if (!native_fn_0200fb90()) {
                            native_data_main_020e5438.field_000c.index = 0;
                            result = RTC_RESULT_SEND_ERROR;
                        }
                    }
                }
            } else {
                native_data_main_020e5438.field_000c.index = 0;
            }
            break;
        case RTC_SEQ_SET_ALARM1_PARAM:
        case RTC_SEQ_SET_ALARM2_PARAM:
        case RTC_SEQ_SET_HOUR_FORMAT:
        case RTC_SEQ_SET_REG_STATUS2:
        case RTC_SEQ_SET_REG_ADJUST:
            break;
        default:
            result = RTC_RESULT_INVALID_COMMAND;
            native_data_main_020e5438.field_000c.index = 0;
        }
    } else {
        native_data_main_020e5438.field_000c.index = 0;
        switch (pxiresult) {
        case RTC_PXI_RESULT_INVALID_COMMAND:
            result = RTC_RESULT_INVALID_COMMAND;
            break;
        case RTC_PXI_RESULT_ILLEGAL_STATUS:
            result = RTC_RESULT_ILLEGAL_STATUS;
            break;
        case RTC_PXI_RESULT_BUSY:
            result = RTC_RESULT_BUSY;
            break;
        case RTC_PXI_RESULT_FATAL_ERROR:
        default:
            result = RTC_RESULT_FATAL_ERROR;
        }
    }
    if (native_data_main_020e5438.field_000c.index == 0) {
        if (native_data_main_020e5438.field_000c.lock != RTC_LOCK_OFF) {
            native_data_main_020e5438.field_000c.lock = RTC_LOCK_OFF;
        }
        if (native_data_main_020e5438.field_000c.callback) {
            cb = native_data_main_020e5438.field_000c.callback;
            native_data_main_020e5438.field_000c.callback = ((void *)0) ;
            cb(result, native_data_main_020e5438.field_000c.callbackArg);
        }
    }
}
