#include "context.h"
s32 native_ov001_02223f20(u32 *words)
{
    s32 index;
    s32 count;
    count = 0;
    index = 0;
    do {
        if (words[index] != 0)
            count++;
        index++;
    } while (index < 3);
    return count;
}
