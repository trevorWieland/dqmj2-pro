#include "context.h"
u32 native_ov000_021db92c(s32 needle, u32 indices, s32 count)
{
    s32 index;
    u32 found;
    found = 0;
    index = 0;
    if (count > 0) {
        do {
            if (needle == *(s16 *) (indices + (u32) index * 2U)) {
                found = 1;
                break;
            }
            index++;
        } while (index < count);
    }
    return found;
}
