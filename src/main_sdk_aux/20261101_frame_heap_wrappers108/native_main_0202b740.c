#include "native_frame_heap_wrapper_types.h"
u32 native_main_0202b740(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 temp_r1;

    temp_r1 = (arg1 + arg0) & ~3;
    temp_r0 = (arg0 + 3) & ~3;
    if ((temp_r0 > temp_r1) || ((u32) (temp_r1 - temp_r0) < 0x30U)) {
        return 0U;
    }
    return native_fn_0202b54c((void *) temp_r0, temp_r1, arg2);
}
