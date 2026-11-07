#include "../../resource_path_api.h"
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0202a250(void);
extern u32 native_fn_0202a37c(u32 heap, u32 bytes, s32 alignment);
extern u32 native_fn_0202a818(u32 path, u32 buffer, u32 bytes, u32 offset);
extern u32 native_fn_0202a498(s32 heap, u32 buffer);

u32 native_main_0203cb8c(u32 path, u32 heap, u32 selector) {
    u32 bytes;
    u32 buffer = 0;
    bytes = native_fn_0202a8e0((const void *)path);
    if (bytes != 0) {
        if (heap == 0xFFFFFFFF) {
            heap = native_fn_0202a250();
        }
        if (selector == 0) {
            buffer = native_fn_0202a37c(heap, (bytes + 3) & ~3U, 4);
        } else {
            buffer = native_fn_0202a37c(heap, (bytes + 3) & ~3U, -4);
        }
        if (buffer != 0) {
            if (native_fn_0202a818(path, buffer, bytes, 0) == 0) {
                native_fn_0202a498((s32)heap, buffer);
                buffer = 0;
            }
        }
    }
    return buffer;
}
