#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027f0e64(u16 *pMacAdrs)
{
    LPCAM_ELEMENT pCAM = (LPCAM_ELEMENT)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.pCAM;
    u32 i;
    if (pMacAdrs[0] & 0x0001) {
        for (i = 1, pCAM++; i < ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MaxStaNum; i++, pCAM++) {
            native_host_arm7_arm_027f0d6c(i);
        }
    }
    else {
        i = native_host_arm7_arm_027eb90c(pMacAdrs);
        if (i != 255 ) {
            native_host_arm7_arm_027f0d6c(i);
        }
        if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Mode == 1 ) && (native_host_arm7_arm_027ebfec(i) == 0x40 )) {
            native_host_arm7_arm_027ebc50(i, 0x20 );
            native_host_arm7_arm_027f0b0c();
        }
    }
}
