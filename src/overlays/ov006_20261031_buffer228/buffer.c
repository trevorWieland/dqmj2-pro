#include "context.h"
u32 native_ov006_021e78ac(u32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6, s32 arg7) {
    u16 buffer[64];

    native_fn_02008be0(0, buffer, 0x80);
    native_fn_020877bc(arg1, buffer, 0x80, arg2);
    return native_fn_ov006_021e775c(arg0, buffer, arg3, arg4, arg5, arg6, arg7);
}
