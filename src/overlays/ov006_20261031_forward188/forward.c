#include "context.h"
u32 native_ov006_021e7824(u32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6) {
    u16 spC[64];

    native_fn_02008be0(0, spC, 0x80);
    native_fn_02046af4(native_data_021c9698, arg1, (u8) arg4, 0, spC, 0xFF);
    return native_fn_ov006_021e775c(arg0, spC, arg2, arg3, arg4, arg5, arg6);
}
