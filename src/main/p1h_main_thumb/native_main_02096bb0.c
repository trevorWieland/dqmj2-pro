#include "context.h"

/* True when the first ten bytes are printable ASCII. */
u32 native_main_02096bb0(const u8 *text)
{
    s32 index;

    for (index = 0; index < 0x0a; index++) {
        u8 current = text[index];

        if (current < 0x20 || current > 0x7e)
            return 0;
    }
    return 1;
}
