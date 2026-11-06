#include "context.h"
u32 native_ov006_021ede18(u32 *output, u32 input, u32 count)
{
    *output = count;
    return native_fn_ov006_021edd68(input, (u32) (output + 1), count);
}
