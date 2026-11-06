#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e5e0c(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    u32 wlBuf[128];
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WlParamSetCfm *pConfirm;
    u16 tableNumber, camLifeTime, frameLifeTime, mpLifeTime;
    tableNumber = (u16)(buf[1]);
    camLifeTime = (u16)(buf[2]);
    frameLifeTime = (u16)(buf[3]);
    mpLifeTime = (u16)(buf[4]);
    pConfirm = native_utility_child_arm7_arm_027e24d4((u16 *)wlBuf, tableNumber, camLifeTime, frameLifeTime);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e5dd0((0x0200 | 0x11) , pConfirm->resultCode);
        return;
    }
    if (mpLifeTime != 0xffff) {
        OSTick mpLifeTimeTick;
        if (mpLifeTime == 0) {
            mpLifeTimeTick = 1;
        } else {
            mpLifeTimeTick = ((OSTick)(((33514000 / 1000) * (u64)(mpLifeTime * 100)) / 64)) ;
        }
        status->mp_lifeTimeTick = mpLifeTimeTick;
    } else {
        status->mp_lifeTimeTick = 0ULL;
    }
    {
        OSTick now = native_utility_child_arm7_arm_037fd724() | 1;
        int i;
        for (i = 0; i < 1 + 15 ; i++) {
            status->mp_lastRecvTick[i] = now;
        }
    }
    {
        WMCallback *cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_SET_LIFETIME;
        cb->errcode = WM_ERRCODE_SUCCESS;
        native_utility_child_arm7_arm_038057c8((void *)cb);
    }
    return;
}
#include "dependency002.h"
