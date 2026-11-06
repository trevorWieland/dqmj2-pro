#include "context.h"
u32 native_ov006_021efa70(u8 *output)
{
    u8 *end;
    u32 count;
    output[0] = 0;
    output[1] = 0;
    output[2] = 0;
    output[3] = 0;
    output[4] = 0;
    output[5] = 0;
    output[6] = 0;
    output[7] = 0;
    end = native_fn_ov006_021efa10(output + 8);
    count = (u32) (end - output);
    *(u16 *) output = (u16) (count - 8);
    return count;
}
