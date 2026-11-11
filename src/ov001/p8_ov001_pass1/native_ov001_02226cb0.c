#include "context.h"
s32 native_ov001_02226cb0(u32 *words)
{
    s32 index = 0;
    do {
        if (words[index] != 0)
            return index;
        index++;
    } while (index < 3);
    return 0;
}
