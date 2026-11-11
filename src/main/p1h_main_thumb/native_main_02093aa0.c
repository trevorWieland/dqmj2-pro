#include "context.h"

/* Propagate a 16-bit addend through the array from the given index. */
void native_main_02093aa0(u16 *array, u32 value, s32 index, s32 limit)
{
    u16 *slot = array + index;

    while (value != 0 && index < limit) {
        u32 sum = value + *slot;

        *slot = (u16)sum;
        value = sum >> 16;
        index++;
        slot++;
    }
}
