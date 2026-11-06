#include "context.h"
u32 native_main_02049794(u32 arg0, s32 arg1, u32 arg2, u32 arg3, u8 arg4, u8 arg5, u8 arg6, u8 arg7, s8 arg8, u32 arg9) {
    u32 *temp_r0;
    u32 resource;

    temp_r0 = native_fn_02049aa8(arg1);
    if (*temp_r0 != 0) {
        return 0U;
    }
    resource = native_fn_0204975c();
    native_fn_02049be4(temp_r0, arg0, arg2, arg3, (u32) (u8) arg4, (u32) (u8) arg5, (u32) (u8) arg6, (u32) (u8) arg7, resource, (s32) (s8) arg8, arg9);
    if (arg9 != 0) {
        native_fn_0204977c((u8) arg6 * (u8) arg7);
    }
    return 1U;
}
