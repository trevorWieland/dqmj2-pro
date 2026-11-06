#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e3538(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMStartParentCallback *cb;
    WlCmdCfm *pConfirm;
    u16 ssidLength;
    BOOL powerSave;
    if (status->state != WM_STATE_IDLE) {
        WMStartParentCallback *callback = (WMStartParentCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_PARENT;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        callback->state = WM_STATECODE_PARENT_START;
        native_utility_child_arm7_arm_038057c8(callback);
        return;
    }
    powerSave = (BOOL)(((u32 *)msg)[1]);
    if (!(status->allowedChannel & ((0x0001 << status->pparam.channel) >> 1))) {
        cb = native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_START_PARENT;
        cb->errcode = WM_ERRCODE_INVALID_PARAM;
        cb->state = WM_STATECODE_PARENT_START;
        native_utility_child_arm7_arm_038057c8(cb);
        return;
    }
    status->mode = 1 ;
    status->aid = 0;
    {
        OSIntrMode e = native_utility_child_arm7_arm_037fe41c();
        status->child_bitmap = 0;
        status->mp_readyBitmap = 0;
        (void)native_utility_child_arm7_arm_037fe430(e);
    }
    status->preamble = 1 ;
    if (!native_utility_child_arm7_arm_027e03b8(WM_APIID_START_PARENT, buf)) {
        return;
    }
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2238(buf);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e34f4((0x0300 | 0x03) , pConfirm->resultCode);
        return;
    }
    {
        u16 pwrMgtMode;
        pwrMgtMode = (u16)(powerSave ? 1 : 0 );
        pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2d80(buf,
            pwrMgtMode,
            0 ,
            1 );
        if (pConfirm->resultCode != 0x00 ) {
            native_utility_child_arm7_arm_027e34f4((0x0000 | 0x01) , pConfirm->resultCode);
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
        native_utility_child_arm7_arm_027e0504(&GameInfo, pparam);
        MI_CpuClear16(ssid, sizeof(u8) * 32 );
        ssid[0] = (u16)(pparam->ggid & 0x0ffff);
        ssid[1] = (u16)(pparam->ggid >> 16);
        ssid[2] = pparam->tgid;
        ssid[3] = 0;
        ssidLength = 32;
        pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e29e4(buf,
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
            native_utility_child_arm7_arm_027e34f4((0x0000 | 0x09) , pConfirm->resultCode);
            return;
        }
        native_utility_child_arm7_arm_027e00b0((u16)(pparam->parentMaxSize
            + ((pparam->KS_Flag)
                    ? (2 * 16 + 4) + (2 + 4)
                    : 0)));
        native_utility_child_arm7_arm_027e0060((u16)(pparam->childMaxSize
            + ((pparam->KS_Flag)
                    ? 2 + (2 + 2)
                    : 0)));
    }
    cb = (WMStartParentCallback *)native_utility_child_arm7_arm_0380576c();
    status->state = WM_STATE_PARENT;
    cb->apiid = WM_APIID_START_PARENT;
    cb->errcode = WM_ERRCODE_SUCCESS;
    cb->state = WM_STATECODE_PARENT_START;
    cb->parentSize = status->mp_parentSize;
    cb->childSize = status->mp_childSize;
    native_utility_child_arm7_arm_038057c8((void *)cb);
    status->beaconIndicateFlag = 1;
    return;
}
#include "dependency002.h"
