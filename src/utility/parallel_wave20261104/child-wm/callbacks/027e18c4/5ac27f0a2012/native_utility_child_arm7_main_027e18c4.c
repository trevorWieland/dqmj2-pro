#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e18c4(WlCmdReq *req)
{
    u16 i;
    WMStatus *status = WMSP_GetStatusStructure();
    WMStartMPCallback *callback;
    WlMaMpEndInd *pInd = (WlMaMpEndInd *)req;
    WMMpRecvHeader *bufp;
    WMMpRecvData *datap;
    OSIntrMode enabled;
    BOOL kick;
    BOOL retryFlag = 0 ;
    u32 size;
    OSTick now;
    u16 errBitmap;
    u32 recvErrorBitmap;
    if (status->mp_flag == 0 ) {
        return;
    }
    ((void)0) ;
    errBitmap = pInd->mpKey.errBitmap;
    if (errBitmap != 0 || (status->mp_resumeFlag == 1 && pInd->mpKey.bitmap != 0)) {
        if (errBitmap != 0) {
            ((void) 0) ;
        }
        native_utility_child_arm7_arm_027e1844();
        return;
    }
    if (status->mp_resumeFlag != 0 ) {
        status->mp_resumeFlag = 0 ;
    }
    bufp = (WMMpRecvHeader *)status->mp_recvBuf[status->mp_recvBufSel];
    size = pInd->mpKey.length * pInd->mpKey.count + sizeof(WMMpRecvHeader) - sizeof(WMMpRecvData);
    if (status->mp_recvBufSize < size) {
        ((void)0)
            ;
        size = status->mp_recvBufSize;
    }
    native_utility_child_arm7_arm_037fe814(&(pInd->mpKey),
        bufp,
        size
    );
    native_utility_child_arm7_arm_027e1728(pInd, bufp->bitmap, status->mp_minPollBmpMode);
    now = native_utility_child_arm7_arm_037fd724() | 1;
    datap = bufp->data;
    recvErrorBitmap = bufp->bitmap;
    for (i = 0; i < bufp->count; ++i, datap = (WMMpRecvData *)(((u32)datap) + bufp->length)) {
        u16 aid = datap->aid;
        u16 length = datap->length;
        if (aid < 1 || 15 < aid) {
            continue;
        }
        if (length >= 2 && length != 0xffff) {
            datap->length -= 2;
            length -= 2;
            status->mp_readyBitmap |= (1 << aid);
            status->mp_lastRecvTick[aid] = now;
            if (length != 0) {
                native_utility_child_arm7_arm_027e6b6c(aid, datap->wmHeader, datap->cdata, length, (WMMpRecvBuf *)bufp);
            }
        } else if (length == 0) {
            OSTick last = status->mp_lastRecvTick[aid];
            recvErrorBitmap |= (1 << aid);
            if (status->mp_lifeTimeTick != 0ULL && last != 0ULL
                && (now - last) > status->mp_lifeTimeTick) {
                u32 *buf = native_utility_child_arm7_arm_027e0134();
                BOOL result;
                ((void) 0) ;
                status->mp_lastRecvTick[aid] = 0ULL;
                if (buf == ((void *)0) ) {
                    result = 0 ;
                } else {
                    buf[0] = WM_APIID_AUTO_DISCONNECT;
                    buf[1] = (u32)(1 << aid);
                    buf[2] = WM_DISCONNECT_REASON_MP_LIFETIME;
                    ((void)0) ;
                    result = native_utility_child_arm7_arm_037fcccc(&(WMSP_GetSystemWork()->requestQ),
                        (OSMessage)buf,
                        0 );
                }
                if (!result) {
                    WMIndCallback *cb = (WMIndCallback *)native_utility_child_arm7_arm_0380576c();
                    cb->apiid = WM_APIID_INDICATION;
                    cb->errcode = WM_ERRCODE_FIFO_ERROR;
                    cb->state = WM_STATECODE_FIFO_ERROR;
                    cb->reason = WM_APIID_AUTO_DISCONNECT;
                    native_utility_child_arm7_arm_038057c8(cb);
                }
            }
        }
    }
    (void)native_utility_child_arm7_arm_027e7018(0 , (u16)recvErrorBitmap);
    if (bufp->bitmap != 0) {
        retryFlag = 1 ;
    }
    callback = (WMStartMPCallback *)native_utility_child_arm7_arm_0380576c();
    callback->apiid = WM_APIID_START_MP;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_MPEND_IND;
    callback->recvBuf = (WMMpRecvBuf *)bufp;
    native_utility_child_arm7_arm_038057c8(callback);
    status->mp_recvBufSel ^= 1;
    enabled = native_utility_child_arm7_arm_037fe41c();
    if (retryFlag == 0 ) {
        status->mp_count--;
    }
    if (status->mp_limitCount > 0) {
        status->mp_limitCount--;
    }
    kick = (status->mp_count > 0 && status->mp_limitCount > 0);
    (void)native_utility_child_arm7_arm_037fe430(enabled);
    if (kick) {
        u16 pollbmp;
        if (retryFlag == 1 ) {
            pollbmp = pInd->mpKey.bitmap;
        } else {
            pollbmp = 0xffff;
        }
        if (status->mp_parentInterval != 0) {
            WmspCancelMPIntervalAlarm();
            native_utility_child_arm7_arm_037fdb1c(
                &native_utility_child_arm7_data_0380933c,
                status->mp_parentIntervalTick,
                native_utility_child_arm7_arm_027e1830,
                (void *)pollbmp);
        } else {
            native_utility_child_arm7_arm_027e17a8(pollbmp);
        }
    }
    ((void)0) ;
}
#include "dependency002.h"
