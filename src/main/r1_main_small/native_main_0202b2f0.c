/* Frame-heap range check: align the span, reject under 0x4c bytes, else allocate.
   Unknowns: the heap descriptor layout and the allocator contract. */
#include "context.h"
extern u32 native_fn_0202b54c(void *,u32,u32);
extern u32 native_fn_0202b594(void *,u32,u32);
extern u32 native_fn_0202b614(void *,u32,u32);

u32 native_main_0202b2f0(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 temp_r1;

    temp_r1 = (arg1 + arg0) & ~3;
    temp_r0 = (arg0 + 3) & ~3;
    if ((temp_r0 > temp_r1) || ((u32) (temp_r1 - temp_r0) < 0x4cU)) {
        return 0U;
    }
    return native_fn_0202ae28((void *) temp_r0, temp_r1, arg2);
}