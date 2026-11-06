#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ebdb4(u32 camAdrs)
{
    ;
    if (native_host_arm7_arm_027ebfec(camAdrs) == 0x40 ) {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.PowerState &= ~(1 << camAdrs);
    }
}

#include "context002.h"
