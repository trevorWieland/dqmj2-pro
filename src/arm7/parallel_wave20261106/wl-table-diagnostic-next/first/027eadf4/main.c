#include "context000.h"

u16 native_host_arm7_main_027eadf4(u8 data, u16 total)
{
    u16 r1;
    r1 = native_host_arm7_data_027f72cc[total & 0xf];
    total = (total >> 4) & 0x0FFF;
    total = total ^ r1 ^ native_host_arm7_data_027f72cc[data & 0xf];
    r1 = native_host_arm7_data_027f72cc[total & 0xf];
    total = (total >> 4) & 0x0fff;
    total = total ^ r1 ^ native_host_arm7_data_027f72cc[(data >> 4) & 0xf];
    return total;
}
