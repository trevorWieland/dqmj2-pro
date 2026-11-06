#include "context.h"
u32 native_main_02028af4(ResourceContext *output)
{
    u32 result = 0;
    if (output->field38 & 1) {
        if (output->resource) native_fn_020321dc(output->resource);
        result |= 1;
    }
    if (output->field38 & 2) {
        if (output->auxiliary08) native_fn_020321dc(output->auxiliary08);
        if (output->animationCount0f) native_fn_0203c00c(output->animation10);
        result |= 2;
    }
    output->field38 = 0;
    return result;
}
