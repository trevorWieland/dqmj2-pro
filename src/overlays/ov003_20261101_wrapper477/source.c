#include "context.h"
u32 native_ov003_021de9f0(s32 arg0, u32 arg1, u32 arg2, u32 arg3, s16 arg4) {
    void **temp_r0;
    void *temp_r4;

    temp_r0 = (void **) native_fn_02049ad0(arg0);
    temp_r4 = M2C_FIELD(*temp_r0, void **, 4);
    native_fn_02049f4c(temp_r0);
    native_fn_0204a04c(temp_r4, arg1, arg2, arg3);
    return native_fn_02085270(temp_r4 + 0x3C, arg4, 0);
}
