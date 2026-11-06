#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e13e4(WlCmdReq *req)
{
    WMStartMPCallback *callback;
    WlMaMpInd *pInd = (WlMaMpInd *)req;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMMpRecvBuf *bufp;
    OSIntrMode enabled;
    BOOL timeout;
    u16 oldSentFlag, oldEmptyFlag;
    BOOL polled;
    u32 size;
    u16 txKeySts;
    {
        u16 rssi8;
        rssi8 = WMSP_GetRssi8(pInd->frame.rssi);
        if (status->minRssi > rssi8) {
            status->minRssi = rssi8;
        }
    }
    if (status->mp_flag == 0 ) {
        return;
    }
    ((void)0)        ;
    if (status->mp_vsyncFlag == 1 ) {
        ((void) 0) ;
        status->mp_vsyncFlag = 0 ;
    }
    oldEmptyFlag = status->mp_bufferEmptyFlag;
    oldSentFlag = status->mp_sentDataFlag;
    status->mp_recvBufSel ^= 1;
    bufp = status->mp_recvBuf[status->mp_recvBufSel];
    size = pInd->frame.length + sizeof(WMMpRecvBuf) - 6U;
    if (status->mp_recvBufSize < size) {
        ((void)0)
            ;
        size = status->mp_recvBufSize;
    }
    native_utility_child_arm7_arm_037fe814(&(pInd->frame),
        bufp,
        size
    );
    enabled = native_utility_child_arm7_arm_037fe41c();
    timeout = 0 ;
    if (status->mp_waitAckFlag == 1 ) {
        timeout = 1 ;
        WmspCancelMPAckAlarm();
        ((void) 0) ;
    }
    status->mp_waitAckFlag = 1 ;
    status->mp_ackTime = bufp->ackTimeStamp;
    txKeySts = pInd->frame.txKeySts;
    polled = ((txKeySts & (0x0001 << 13) ) ? 1 : 0 );
    status->mp_isPolledFlag = (u16)polled;
    native_utility_child_arm7_arm_037fdb1c(
        &native_utility_child_arm7_data_03809310,
        ((OSTick)(((33514000 / 1000) * (u64)(((u16)(bufp->ackTimeStamp - bufp->timeStamp) + 128) << 4)) / 64)) / 1024,
        native_utility_child_arm7_arm_027e1344,
        ((void *)0) );
    {
        BOOL sent, empty;
        empty = ((txKeySts & ((0x0001 << 13) | (0x0001 << 11) )) == ((0x0001 << 13) | (0x0001 << 11) ));
        sent = ((txKeySts & ((0x0001 << 13) | (0x0001 << 14) )) == ((0x0001 << 13) | (0x0001 << 14) ));
        if (sent) {
            status->mp_setDataFlag = 0 ;
        }
        status->mp_bufferEmptyFlag = (u16)((empty) ? 1 : 0 );
        status->mp_sentDataFlag = (u16)((sent) ? 1 : 0 );
    }
    if (polled) {
        s32 childSize;
        childSize = ((((s32)bufp->txop - 96 - 6) / 4) - 24 - 4 - 2 - 2 );
        if (childSize >= 0) {
            if (childSize > status->mp_childMaxSize) {
                childSize = status->mp_childMaxSize;
            }
            if (childSize != status->mp_childSize) {
                ((void)0) ;
                native_utility_child_arm7_arm_027e0000((u16)childSize);
            }
        }
    }
    (void)native_utility_child_arm7_arm_037fe430(enabled);
    if (timeout) {
        if (oldEmptyFlag == 1 ) {
            (void)native_utility_child_arm7_arm_027e7018(timeout, 0x0000);
        }
        callback = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_MP;
        callback->errcode = WM_ERRCODE_TIMEOUT;
        callback->state = WM_STATECODE_MPACK_IND;
        callback->recvBuf = ((void *)0) ;
        native_utility_child_arm7_arm_038057c8(callback);
    }
    if (!polled) {
        if (bufp->length >= 2) {
            status->mp_vsyncOrderedFlag = ((bufp->wmHeader & 0x8000 ) != 0);
        }
        ((void)0) ;
        return;
    }
    native_utility_child_arm7_arm_037fe814(pInd->frame.destAdrs, bufp->destAdrs, 6 );
    native_utility_child_arm7_arm_037fe814(pInd->frame.srcAdrs, bufp->srcAdrs, 6 );
    if (bufp->length >= 2) {
        bufp->length -= 2;
        status->mp_vsyncOrderedFlag = ((bufp->wmHeader & 0x8000 ) != 0);
        callback = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_MP;
        callback->errcode = WM_ERRCODE_SUCCESS;
        callback->state = WM_STATECODE_MP_IND;
        callback->recvBuf = bufp;
        native_utility_child_arm7_arm_038057c8(callback);
        if (bufp->length > 0) {
            native_utility_child_arm7_arm_027e6b6c(0, bufp->wmHeader, bufp->data, bufp->length, bufp);
        }
    } else {
        bufp->length = 0;
        status->mp_vsyncOrderedFlag = 0 ;
        callback = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_MP;
        callback->errcode = WM_ERRCODE_NO_DATA;
        callback->state = WM_STATECODE_MP_IND;
        callback->recvBuf = bufp;
        native_utility_child_arm7_arm_038057c8(callback);
    }
    if (status->mp_lifeTimeTick != 0ULL) {
        status->mp_lastRecvTick[0] = native_utility_child_arm7_arm_037fd724() | 1;
    }
    ((void)0) ;
}
#include "dependency002.h"
