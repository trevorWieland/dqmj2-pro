#include "native_frame_heap_wrapper_types.h"
u32 native_main_0202b784(u32 arg0, u32 arg1, u32 arg2) {
    void *temp_r0;
    s32 temp_r1;
    u32 var_r1;

    var_r1 = arg1;
    if (var_r1 == 0) {
        var_r1 = 1;
    }
    temp_r1 = (var_r1 + 3) & ~3;
    temp_r0 = (void *)(arg0 + 0x24);
    if ((s32) arg2 >= 0) {
        return native_fn_0202b594(temp_r0, temp_r1, (s32) arg2);
    }
    return native_fn_0202b614(temp_r0, temp_r1, 0 - arg2);
}
