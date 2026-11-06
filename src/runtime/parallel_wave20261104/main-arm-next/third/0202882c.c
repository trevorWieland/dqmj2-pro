#include "context.h"
u32 native_main_0202882c(ResourceContext *output, ResourceHeader *resource)
{
    u32 result = 0;
    u32 signature;
    u32 size0;
    u32 size1;
    u32 size2;
    u32 failed;
    TextureView *texture;
    u32 key0;
    u32 key1;
    u32 key2;
    output->field4c = output->field50 = output->field54 = 0;
    signature = resource->signature;
    if (signature == 0x30585442 || signature == 0x30444d42) {
        texture = native_fn_0202beec(resource);
        if (texture) {
            size0 = native_fn_0202ec30(texture);
            size1 = native_fn_0202ec44(texture);
            size2 = native_fn_0202ed70(texture);
            key0 = key1 = key2 = 0;
            failed = 0;
            if (size0) {
                key0 = native_data_020dd8c0(size0, 0, 0);
                if (!key0) failed |= 1;
            }
            if (size1) {
                key1 = native_data_020dd8c0(size1, 1, 0);
                if (!key1) failed |= 2;
            }
            if (size2) {
                key2 = native_data_020dd8b8(size2, texture->flags20 & 0x8000, 0);
                if (!key2) failed |= 4;
            }
            if (!failed) {
                native_fn_0202ec58(texture, key0, key1);
                native_fn_0202ed84(texture, key2);
                output->texture3c = texture;
                output->key40 = key0;
                output->field4c = size0;
                output->key44 = key1;
                output->field50 = size1;
                output->key48 = key2;
                output->field54 = size2;
                result = 1;
                if (signature == 0x30444d42) {
                    void *model = native_fn_0202bedc(resource);
                    if (model) native_fn_0202f3dc(model, texture);
                    else result = 0;
                }
            }
        }
    }
    return result;
}
