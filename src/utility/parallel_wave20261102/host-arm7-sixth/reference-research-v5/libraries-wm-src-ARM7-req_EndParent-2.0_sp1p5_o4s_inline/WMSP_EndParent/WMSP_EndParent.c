#include "context000.h"

#include "context001.h"

void WMSP_EndParent(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WMCallback *cb;
    WlCmdCfm *pConfirm;
    if (status->state != WM_STATE_PARENT) {
        WMCallback *callback = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        callback->apiid = WM_APIID_END_PARENT;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        WMSP_ReturnResult2Wm9(callback);
        return;
    }
    status->pparam.entryFlag = 0 ;
    {
        u16 wMac[3];
        s32 i;
        OSIntrMode e;
        for (i = 1; i < (15 + 1); i++) {
            if (status->child_bitmap & (0x0001 << i)) {
                MI_CpuCopy8(status->childMacAddress[i - 1], wMac, 6 );
                {
                    s32 auth_retry;
                    for (auth_retry = 0; auth_retry < 2 ;) {
                        pConfirm = (WlCmdCfm *)WMSP_WL_MlmeDeAuthenticate((u16 *)wlBuf, wMac, 3 );
                        switch (pConfirm->resultCode) {
                        case 0x00 :
                            break;
                        case 0x07 :
                        case 0x0C :
                            auth_retry++;
                            continue;
                        default:
                            break;
                        }
                        break;
                    }
                }
                e = OS_DisableInterrupts();
                if (status->child_bitmap & (0x0001 << i)) {
                    status->child_bitmap &= ~(0x0001 << i);
                    status->mp_readyBitmap &= ~(0x0001 << i);
                    status->mp_lastRecvTick[i] = 0ULL;
                    (void)OS_RestoreInterrupts(e);
                    WMSP_IndicateDisconnectionFromMyself(1 , (u16)i, wMac);
                } else {
                    (void)OS_RestoreInterrupts(e);
                }
            }
        }
    }
    pConfirm = (WlCmdCfm *)WMSP_WL_MlmeReset((u16 *)wlBuf, 1 );
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0000 | 0x00) , pConfirm->resultCode);
        return;
    }
    status->beaconIndicateFlag = 0;
    status->state = WM_STATE_CLASS1;
    pConfirm = (WlCmdCfm *)WMSP_WL_DevIdle((u16 *)wlBuf);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0300 | 0x02) , pConfirm->resultCode);
        return;
    }
    status->state = WM_STATE_IDLE;
    status->wep_flag = 0 ;
    status->wepMode = 0 ;
    MI_CpuClear8(status->wepKey, 80 );
    WMSP_ResetSizeVars();
    cb = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
    cb->apiid = WM_APIID_END_PARENT;
    cb->errcode = WM_ERRCODE_SUCCESS;
    WMSP_ReturnResult2Wm9((void *)cb);
    return;
}

#include "context002.h"
