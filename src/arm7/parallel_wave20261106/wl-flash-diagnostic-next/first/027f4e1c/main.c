#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027f4e1c(u32 adrs, u32 size, u8 *pBuf)
{
    u8 *p;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg == (0) ) {
        return;
    }
    p = (u8 *)((u32)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg + adrs - 0x002a );
    while (size > 0) {
        native_host_arm7_arm_027ead30(pBuf++, native_host_arm7_arm_027ead5c(p++));
        size--;
    }
}
