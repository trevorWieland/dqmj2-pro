#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e0520(u8 rssi8)
{
    native_host_arm7_data_027f7884.rssiHistory[native_host_arm7_data_027f7884.rssiIndex] = rssi8;
    native_host_arm7_data_027f7884.rssiIndex = (u32)((native_host_arm7_data_027f7884.rssiIndex + 1) % 32 );
    WMSP_AddRssiToRandomPool(rssi8);
}
