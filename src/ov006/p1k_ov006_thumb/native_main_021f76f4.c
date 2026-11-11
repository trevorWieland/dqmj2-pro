#include "context.h"

extern u16 native_data_027fffa8;

/* Report whether the low battery bit is set. */
u32 native_main_021f76f4(void)
{
    if (((s32)(native_data_027fffa8 & 0x8000)) >> 15)
        return 1;
    return 0;
}
