#include "context.h"

extern u32 native_fn_02093874(const u16 *array, u32 count);

/* Flag a terminator halfword as invalid, otherwise report whether the array
   still has a trailing nonzero entry. */
s32 native_main_02093890(const u16 *array, u32 count)
{
    if ((array[count - 1] & 0x8000) != 0)
        return -1;
    if (native_fn_02093874(array, count) != 0)
        return 1;
    return 0;
}

