#include "context.h"

extern u8 native_data_020e33e4[];

extern void native_fn_0208dcb8(u32 resource, u32 arg1, u32 arg2, u32 arg3);

/* Release one queued resource from the active record. */
void native_main_0208ddd4(void)
{
    u8 *state = *(u8 **)(native_data_020e33e4 + 4);
    u32 *record = *(u32 **)(state + 0xa4);

    if (record == 0)
        return;
    if (record[0x18] == 0)
        return;
    native_fn_0208dcb8(record[0x17], record[0x18], 0, 0);
    record[0x18] = 0;
}
