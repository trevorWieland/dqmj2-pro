#include "context.h"

extern u8 native_data_021d18e0[];
extern u32 native_fn_02012824(u32 argument);

/* Arm the mode-3 record path and hand the argument to the ARM dispatcher. */
s32 native_main_02096734(u32 argument)
{
    u32 *record;
    u32 result;

    if (argument == 0)
        return -1;
    record = *(u32 **)native_data_021d18e0;
    *(u32 *)((u8 *)record + 0x1a90) = 3;
    *(u32 **)native_data_021d18e0 = 0;
    result = native_fn_02012824(argument);
    if (result == 2)
        return 0;
    return (s32)result;
}
