#include "context.h"

extern u16 native_data_027fffa8;

/* Report bit 15 of the shared status word. */
u32 native_main_021fbabc(void)
{
    if (((s32)(native_data_027fffa8 & 0x8000)) >> 15)
        return 1;
    return 0;
}
