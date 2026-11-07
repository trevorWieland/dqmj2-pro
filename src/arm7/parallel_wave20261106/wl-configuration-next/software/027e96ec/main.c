#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e96ec(u16 period)
{
    if ((period < 10 ) || (period > 1000 )) {
        return 0x05 ;
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.BeaconPeriod = period;
    *(vu16 *)((0x04808000) + 0x08C) = period;
    native_host_arm7_arm_027e9e3c(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.FrameLifeTimePerBeacon);
    return 0;
}

#include "context002.h"
