#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ebc50(u16 camAdrs, u16 state)
{
    u32 x;
    ;
    x = native_host_arm7_arm_037fb928((1UL << 24) );
    if (state < 0x40 ) {
        CAM_SetAwake(camAdrs);
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.NotClass3 |= (1 << camAdrs);
        if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.Mode == 1 ) && (native_host_arm7_arm_027ec0d8(camAdrs) != 0)) {
            native_host_arm7_arm_027ebf6c(camAdrs);
        }
    } else {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.NotClass3 &= ~(1 << camAdrs);
        if (CAM_GetPowerMgtMode(camAdrs)) {
            native_host_arm7_main_027ebdb4(camAdrs);
        }
    }
    CAM_GetTbl(camAdrs)->state = state;
    native_host_arm7_arm_037fb8f0(x);
}

#include "context002.h"
