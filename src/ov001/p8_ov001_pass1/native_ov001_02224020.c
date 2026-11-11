#include "context.h"
void native_ov001_02224020(u32 *out, u8 *group)
{
    s32 index = 0;
    do {
        if (group[0x31C] == 0 || group[0x1FF] == 0)
            out[index] = 0;
        group += 0x440;
        index++;
    } while (index < 3);
}
