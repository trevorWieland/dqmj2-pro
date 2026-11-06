#include "context.h"
u32 native_main_02028a4c(ResourceContext *output, ResourceHeader *resource, u32 mode)
{
    u32 result = 0;
    if (resource->signature == 0x30585442 && output->resource) {
        if (mode) {
            if (native_fn_02031fa4(resource)) {
                TextureView *texture = native_fn_0202beec(resource);
                native_fn_0202f3dc(native_fn_0202bedc(output->resource), texture);
                output->auxiliary08 = resource;
                result = 1;
            }
        } else if (native_fn_0202882c(output, resource)) {
            TextureView *texture = native_fn_0202beec(resource);
            native_fn_0202f3dc(native_fn_0202bedc(output->resource), texture);
            output->auxiliary08 = resource;
            result = 1;
        }
    }
    return result;
}
