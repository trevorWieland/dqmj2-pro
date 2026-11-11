#include "context.h"

extern u8 native_data_020e33e4[];

/* Mirror two words into the active display record at +0x814/+0x818. */
void native_main_02090bb8(u32 first, u32 second)
{
    u8 *state = *(u8 **)(native_data_020e33e4 + 4);
    u32 *record;
    u8 *target;

    record = *(u32 **)(state + 0xa4);
    if (record == 0)
        return;
    target = (u8 *)record[3];
    if (target == 0)
        return;
    *(u32 *)(target + 0x814) = first;
    *(u32 *)(target + 0x818) = second;
}
