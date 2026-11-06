#include "context.h"
u32 native_ov006_021edc20(u32 a, u32 b, u32 c, u32 d, u8 *output, u32 value)
{
    *output = (u8) value;
    return native_fn_main_020903f8(a, b, c, d, output);
}
