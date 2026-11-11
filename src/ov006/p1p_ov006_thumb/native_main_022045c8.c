#include "context.h"

/* Bounded string length: stop at NUL or the limit. */
u32 native_main_022045c8(const u8 *text, s32 limit)
{
    s32 index = 0;

    if (limit > 0) {
        do {
            if (text[index] == 0)
                break;
            index++;
        } while (index < limit);
    }
    return (u32)index;
}
