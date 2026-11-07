#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e9e3c(u32 lifeTimePerBeacon)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    if (lifeTimePerBeacon == 0xFFFF) {
        pConfig->FrameLifeTimePerBeacon = 0xFFFF;
        pWork->FrameLifeTime = 0xFFFF;
    } else {
        u32 lifeTime = (u32)lifeTimePerBeacon * (u32)pWork->BeaconPeriod / 100 ;
        if (lifeTime > 0x00010000) {
            return 0x05 ;
        }
        pConfig->FrameLifeTimePerBeacon = lifeTimePerBeacon;
        pWork->FrameLifeTime = lifeTime;
    }
    return 0;
}
