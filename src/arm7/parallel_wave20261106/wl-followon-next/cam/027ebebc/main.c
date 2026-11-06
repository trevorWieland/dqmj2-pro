#include "context000.h"

#include "context001.h"

u32 native_host_arm7_main_027ebebc(u16 camAdrs)
{
    LPCAM_MAN pCamMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan;
    u32 i, map, x;
    ;
    x = native_host_arm7_arm_037fb928((1UL << 24) );
    for (i = 1, map = 2; i < 16; i++, map <<= 1) {
        if ((pCamMan->UseAidMap & map) == 0) {
            pCamMan->UseAidMap |= map;
            pCamMan->ConnectSta++;
            if (pCamMan->ConnectSta == 1) {
                native_host_arm7_arm_027e9eec();
            }
            CAM_GetTbl(camAdrs)->aid = i;
            native_host_arm7_arm_037fb8f0(x);
            return i;
        }
    }
    native_host_arm7_arm_037fb8f0(x);
    return 0;
}

#include "context002.h"
