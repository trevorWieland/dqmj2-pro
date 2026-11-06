#include "context.h"
s32 native_ov006_021ec8f0(u8 *input, s32 count)
{
    s32 index;
    for (index = 0;
    index < count;
    index++) { u32 value = *input++;
    if (value < 0x20 || value > 0x7F) return -1;
    } return 0;
}
