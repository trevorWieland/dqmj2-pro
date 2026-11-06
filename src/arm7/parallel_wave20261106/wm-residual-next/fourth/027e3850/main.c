#include "context000.h"

void native_host_arm7_main_027e3850(u8 rssi8)
{
    u32 rssi_pool = (u32)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool << 1);
    rssi_pool ^= rssi8;
    rssi_pool ^= rssi_pool >> 16;
    ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool = (u16)rssi_pool;
}
