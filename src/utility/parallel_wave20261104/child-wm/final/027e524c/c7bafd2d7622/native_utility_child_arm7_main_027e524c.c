#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e524c(OSMessage msg)
{
    u32 wlBuf[128];
    u32 *buf = (u32 *)msg;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMErrCode err = WM_ERRCODE_SUCCESS;
    WMStartMPReq *req = (WMStartMPReq *)buf;
    WMMpRecvBuf *recvBuf = (WMMpRecvBuf *)req->recvBuf;
    u32 recvBufSize = req->recvBufSize;
    u32 *sendBuf = req->sendBuf;
    u32 sendBufSize = req->sendBufSize;
    WMMPParam *mpParam = &req->param;
    if (status->mp_ignoreSizePrecheckMode == 0 ) {
        if (sendBufSize < WMSP_GetMPSendBufferSize(status->mp_maxSendSize)) {
            err = WM_ERRCODE_INVALID_PARAM;
        }
        if (recvBufSize < ((status->aid == 0) ? WMSP_GetMPOneReceiveBufferSizeParent(status->mp_maxRecvSize, status->pparam.maxEntry) : WMSP_GetMPOneReceiveBufferSizeChild(status->mp_maxRecvSize))) {
            err = WM_ERRCODE_INVALID_PARAM;
        }
    }
    if (status->mode == 2 ) {
        if (!(status->allowedChannel & (0x0001 << sys->wm7buf->connectPInfo.channel) >> 1)) {
            err = WM_ERRCODE_INVALID_PARAM;
        }
    }
    if (err != WM_ERRCODE_SUCCESS) {
        WMStartMPCallback *cb = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_START_MP;
        cb->errcode = err;
        cb->state = WM_STATECODE_MP_START;
        native_utility_child_arm7_arm_038057c8((void *)cb);
        return;
    }
    {
        BOOL fCleanQueue = 0 ;
        OSIntrMode e;
        if (status->mp_flag) {
            status->mp_flag = 0 ;
            fCleanQueue = 1 ;
            ((void)0) ;
        }
        if (fCleanQueue) {
            native_utility_child_arm7_arm_027e6e08(0xffff);
        }
        native_utility_child_arm7_arm_027e7dc8();
        (void)native_utility_child_arm7_arm_027e8570(mpParam, ((void *)0) );
        e = native_utility_child_arm7_arm_037fe41c();
        if ((status->state == WM_STATE_CHILD) || (status->state == WM_STATE_PARENT)) {
            status->mp_waitAckFlag = 0 ;
            status->mp_vsyncOrderedFlag = 0 ;
            status->mp_vsyncFlag = 1 ;
            status->mp_newFrameFlag = 0 ;
            status->mp_pingFlag = 0 ;
            status->mp_pingCounter = 60 ;
            status->sendQueueInUse = 0 ;
            status->mp_setDataFlag = 0 ;
            status->mp_sentDataFlag = 0 ;
            status->mp_bufferEmptyFlag = 0 ;
            status->mp_isPolledFlag = 0 ;
            status->mp_resumeFlag = 0 ;
            status->mp_recvBuf[0] = recvBuf;
            status->mp_recvBufSize = (u16)recvBufSize;
            status->mp_recvBuf[1] = (WMMpRecvBuf *)((u32)recvBuf + recvBufSize);
            status->mp_recvBufSel = 0;
            status->mp_sendBuf = sendBuf;
            status->mp_sendBufSize = (u16)sendBufSize;
            status->mp_count = 0;
            status->mp_limitCount = 0;
            status->mp_prevPollBitmap = 0;
            status->mp_prevWmHeader = 0;
            status->minRssi = 0xffff;
            status->rssiCounter = 1 ;
            {
                OSTick now = native_utility_child_arm7_arm_037fd724() | 1;
                int i;
                for (i = 0; i < (1 + 15 ); i++) {
                    status->mp_lastRecvTick[i] = now;
                }
            }
            native_utility_child_arm7_arm_027e01d8();
            status->valarm_queuedFlag = 0 ;
            native_utility_child_arm7_arm_027e67a4();
            if (status->state == WM_STATE_CHILD) {
                status->state = WM_STATE_MP_CHILD;
            } else if (status->state == WM_STATE_PARENT) {
                status->state = WM_STATE_MP_PARENT;
            }
            {
                WMStartMPCallback *cb = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
                cb->apiid = WM_APIID_START_MP;
                cb->errcode = WM_ERRCODE_SUCCESS;
                cb->state = WM_STATECODE_MP_START;
                native_utility_child_arm7_arm_038057c8((void *)cb);
            }
            status->mp_flag = 1 ;
            (void)native_utility_child_arm7_arm_037fe430(e);
            {
                WlCmdCfm *p_confirm;
                p_confirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e23b4((u16 *)wlBuf, 1);
                if (p_confirm->resultCode != 0x00 ) {
                    WMCallback *cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
                    cb->apiid = WM_APIID_START_MP;
                    cb->errcode = WM_ERRCODE_FAILED;
                    cb->wlCmdID = (0x0200 | 0x16) ;
                    cb->wlResult = p_confirm->resultCode;
                    native_utility_child_arm7_arm_038057c8((void *)cb);
                    return;
                }
            }
            return;
        } else {
            (void)native_utility_child_arm7_arm_037fe430(e);
            {
                WMStartMPCallback *cb = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
                cb->apiid = WM_APIID_START_MP;
                cb->errcode = WM_ERRCODE_ILLEGAL_STATE;
                cb->state = WM_STATECODE_MP_START;
                native_utility_child_arm7_arm_038057c8((void *)cb);
            }
            return;
        }
    }
}
