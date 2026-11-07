#include "context000.h"

u32 native_host_arm7_main_027f65c8(u32 bcd)
{
    u32 hex = 0;
    s32 i;
    s32 w;
    for (i = 0; i < 8; i++) {
        if (((bcd >> (i * 4)) & 0xF) >= 0xA) {
            return hex;
        }
    }
    for (i = 0, w = 1; i < 8; i++, w *= 10) {
        hex += ((bcd >> (i * 4)) & 0xF) * w;
    }
    return hex;
}
