#include "masked_callers.h"
extern u32 native_fn_02049aa8(u32);
extern u32 native_fn_02049f4c(void **);
extern u32 native_fn_02060600(void *,u32,const s16 *,u32);
extern u32 native_fn_02087e44(u32, u32);
u32 native_main_0204a3ec(u32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4) {
    void **temp_r0;
    void *temp_r1;

    temp_r0 = (void **) native_fn_02049aa8(arg0);
    temp_r1 = M2C_FIELD(*temp_r0, void **, 4);
    if (arg4 != 0) {
        native_fn_02087e44(M2C_FIELD(temp_r1, s32 *, 0x44), 0);
    }
    native_fn_02049f4c(temp_r0);
    native_fn_02060600(*temp_r0, arg3, (const s16 *)arg1, (u8)arg2);
    return 0U;
}
