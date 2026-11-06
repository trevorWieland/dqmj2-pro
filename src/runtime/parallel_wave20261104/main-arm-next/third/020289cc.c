#include "context.h"
u32 native_main_020289cc(ResourceContext *output, ResourceHeader *resource, u32 mode)
{
    u32 result = 0;
    if (resource->signature == 0x30444d42) {
        if (mode) result = native_fn_02031fa4(resource);
        else result = native_fn_0202882c(output, resource);
        if (result) {
            output->resource = resource;
            output->field4 = native_fn_0202beec(resource) != 0;
            result = 1;
            output->field38 |= 1;
            output->field39 = 1;
        }
    }
    return result;
}
