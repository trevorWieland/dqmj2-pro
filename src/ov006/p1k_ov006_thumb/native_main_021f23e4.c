#include "context.h"

extern u8 native_data_0221c008[];

/* Clear the active record's mode byte. */
void native_main_021f23e4(void)
{
    u32 *record = *(u32 **)native_data_0221c008;

    *(u8 *)((u8 *)record + 0x18) = 0;
}
