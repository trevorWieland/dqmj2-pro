#include "context.h"

extern u16 native_data_027fffa8;

/* Report bit 15 of the shared status word (same pool word as 0x021fbabc). */
u32 native_main_021fe06c(void)
{
    if (((s32)(native_data_027fffa8 & 0x8000)) >> 15)
        return 1;
    return 0;
}
