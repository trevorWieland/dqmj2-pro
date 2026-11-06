#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e10d4(WlCmdReq *req)
{
    WMstartMPCallback *callback;
    WlMaMpAckInd *pInd = (WlMaMpAckInd *)req;
    WlRxMpAckFrame *pFrame = (WlRxMpAckFrame *)&(pInd->ack);
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    OSIntrMode enabled;
    BOOL failed;
    BOOL timeout;
    BOOL retryFlag = 0 ;
    BOOL sent, empty;
    BOOL polled;
    u16 timeStamp;
    if (status->mp_flag == 0 ) {
        return;
    }
    if (pInd->header.length == 0) {
        u16 lower0, lower1;
        u16 higher;
        timeout = 1 ;
        lower0 = *(vu16 *)((0x04808000) + 0x0F8) ;
        higher = *(vu16 *)((0x04808000) + 0x0FA) ;
        lower1 = *(vu16 *)((0x04808000) + 0x0F8) ;
        if (lower0 > lower1) {
            higher = *(vu16 *)((0x04808000) + 0x0FA) ;
        }
        timeStamp = (u16)((higher << (16 - 4)) | (lower1 >> 4));
        if (!((s16)(timeStamp - status->mp_ackTime) > 0)) {
            ((void) 0) ;
            return;
        }
    } else {
        timeout = 0 ;
    }
    enabled = native_utility_child_arm7_arm_037fe41c();
    if (status->mp_waitAckFlag == 0 ) {
        (void)native_utility_child_arm7_arm_037fe430(enabled);
        ((void)0)
            ;
        return;
    }
    status->mp_waitAckFlag = 0 ;
    polled = status->mp_isPolledFlag;
    WmspCancelMPAckAlarm();
    (void)native_utility_child_arm7_arm_037fe430(enabled);
    sent = status->mp_sentDataFlag;
    failed = !sent || (!timeout && (pFrame->bitmap & (1 << status->aid)));
    if (status->mp_sentDataFlag) {
        status->mp_sentDataFlag = 0 ;
    }
    empty = status->mp_bufferEmptyFlag;
    if (empty) {
        status->mp_bufferEmptyFlag = 0 ;
        retryFlag = native_utility_child_arm7_arm_027e7018(timeout, (u16)((failed) ? 0x0001 : 0x0000));
    }
    ((void)0) ;
    if (!polled) {
        ((void)0) ;
        return;
    }
    callback = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
    callback->apiid = WM_APIID_START_MP;
    if (timeout) {
        callback->errcode = WM_ERRCODE_TIMEOUT;
    } else if (pFrame->bitmap & (1 << status->aid)) {
        callback->errcode = WM_ERRCODE_SEND_FAILED;
    } else {
        callback->errcode = WM_ERRCODE_SUCCESS;
    }
    callback->state = WM_STATECODE_MPACK_IND;
    callback->recvBuf = ((void *)0) ;
    if (!timeout) {
        callback->timeStamp = pFrame->timeStamp;
        callback->rate_rssi = *(u16 *)&(pFrame->rate);
        native_utility_child_arm7_arm_037fe814(pFrame->destAdrs, callback->destAdrs, 6 );
        native_utility_child_arm7_arm_037fe814(pFrame->srcAdrs, callback->srcAdrs, 6 );
        callback->seqNum = pFrame->seqCtrl;
        callback->tmptt = pFrame->tmptt;
        callback->pollbmp = pFrame->bitmap;
    }
    native_utility_child_arm7_arm_038057c8(callback);
    ((void)0) ;
    if (polled) {
        if (retryFlag == 1 || status->mp_vsyncOrderedFlag == 0 ) {
            if (status->mp_childInterval != 0) {
                WmspCancelMPIntervalAlarm();
                native_utility_child_arm7_arm_037fdb1c(
                    &native_utility_child_arm7_data_0380933c,
                    status->mp_childIntervalTick,
                    native_utility_child_arm7_arm_027e10c8,
                    ((void *)0) );
            } else {
                native_utility_child_arm7_arm_027e1038();
            }
        } else {
            status->mp_vsyncOrderedFlag = 0 ;
            status->mp_vsyncFlag = 1 ;
            status->mp_newFrameFlag = 0 ;
        }
    }
}
#include "dependency002.h"
