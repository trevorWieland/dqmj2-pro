#include "context000.h"

#include "context001.h"

void WMSP_StartParent(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMStartParentCallback *cb;
    WlCmdCfm *pConfirm;
    u16 ssidLength;
    BOOL powerSave;
    if (status->state != WM_STATE_IDLE || (status->miscFlags & 0x0001 )) {
        WMStartParentCallback *callback = (WMStartParentCallback *)WMSP_GetBuffer4Callback2Wm9();
        callback->apiid = WM_APIID_START_PARENT;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        callback->state = WM_STATECODE_PARENT_START;
        WMSP_ReturnResult2Wm9(callback);
        return;
    }
    powerSave = (BOOL)(((u32 *)msg)[1]);
    if (!(status->allowedChannel & ((0x0001 << status->pparam.channel) >> 1))) {
        cb = WMSP_GetBuffer4Callback2Wm9();
        cb->apiid = WM_APIID_START_PARENT;
        cb->errcode = WM_ERRCODE_INVALID_PARAM;
        cb->state = WM_STATECODE_PARENT_START;
        WMSP_ReturnResult2Wm9(cb);
        return;
    }
    status->mode = 1 ;
    status->aid = 0;
    {
        OSIntrMode e = OS_DisableInterrupts();
        status->child_bitmap = 0;
        status->mp_readyBitmap = 0;
        (void)OS_RestoreInterrupts(e);
    }
    status->preamble = 1 ;
    if (!WMSP_SetAllParams(WM_APIID_START_PARENT, buf)) {
        return;
    }
    pConfirm = (WlCmdCfm *)WMSP_WL_DevClass1(buf);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0300 | 0x03) , pConfirm->resultCode);
        return;
    }
    {
        u16 pwrMgtMode;
        pwrMgtMode = (u16)(powerSave ? 1 : 0 );
        pConfirm = (WlCmdCfm *)WMSP_WL_MlmePowerManagement(buf,
            pwrMgtMode,
            0 ,
            1 );
        if (pConfirm->resultCode != 0x00 ) {
            WmspError((0x0000 | 0x01) , pConfirm->resultCode);
            return;
        }
        status->pwrMgtMode = pwrMgtMode;
    }
    {
        u16 ssid[32 / sizeof(u16)] __attribute__ ((aligned(2))) ;
        WMParentParam *pparam;
        WMGameInfo GameInfo __attribute__ ((aligned(32))) ;
        pparam = &(status->pparam);
        MI_CpuClear16(&GameInfo, sizeof(WMGameInfo));
        WMSP_CopyParentParam(&GameInfo, pparam);
        MI_CpuClear16(ssid, sizeof(u8) * 32 );
        ssid[0] = (u16)(pparam->ggid & 0x0ffff);
        ssid[1] = (u16)(pparam->ggid >> 16);
        ssid[2] = pparam->tgid;
        ssid[3] = 0;
        ssidLength = 32;
        pConfirm = (WlCmdCfm *)WMSP_WL_MlmeStart(buf,
            ssidLength,
            (u8 *)ssid,
            pparam->beaconPeriod,
            2 ,
            pparam->channel,
            3 ,
            3 ,
            (u16)(16
                + pparam->userGameInfoLength),
            &GameInfo);
        if (pConfirm->resultCode != 0x00 ) {
            WmspError((0x0000 | 0x09) , pConfirm->resultCode);
            return;
        }
        WMSP_SetParentMaxSize((u16)(pparam->parentMaxSize
            + ((pparam->KS_Flag)
                    ? (2 * 16 + 4) + (2 + 4)
                    : 0)));
        WMSP_SetChildMaxSize((u16)(pparam->childMaxSize
            + ((pparam->KS_Flag)
                    ? 2 + (2 + 2)
                    : 0)));
    }
    cb = (WMStartParentCallback *)WMSP_GetBuffer4Callback2Wm9();
    status->state = WM_STATE_PARENT;
    cb->apiid = WM_APIID_START_PARENT;
    cb->errcode = WM_ERRCODE_SUCCESS;
    cb->state = WM_STATECODE_PARENT_START;
    cb->parentSize = status->mp_parentSize;
    cb->childSize = status->mp_childSize;
    WMSP_ReturnResult2Wm9((void *)cb);
    status->beaconIndicateFlag = 1;
    return;
}

#include "context002.h"
