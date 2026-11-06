#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e0374(u8 rssi8)
{
    native_utility_child_arm7_data_027f84f0.rssiHistory[native_utility_child_arm7_data_027f84f0.rssiIndex] = rssi8;
    native_utility_child_arm7_data_027f84f0.rssiIndex = (u32)((native_utility_child_arm7_data_027f84f0.rssiIndex + 1) % 32 );
    WMSP_AddRssiToRandomPool(rssi8);
}
