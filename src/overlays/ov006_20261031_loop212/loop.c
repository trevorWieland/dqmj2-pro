#include "context.h"
u32 native_ov006_021f4f44(s32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r6;

    M2C_FIELD(native_data_ov006_0221c06c, s32 *, 4) = arg0;
    if (native_fn_ov006_021f4fc0(arg1, arg2) == 0) {
        return -1U;
    }
    temp_r6 = native_fn_0209747c();
    native_fn_02097470((u32) native_data_ov006_0220d974);
    M2C_FIELD(native_data_ov006_0221c06c, u8 *, 1) = 0U;
    native_fn_ov006_021f5010();
    native_fn_ov006_021f50b0();
    native_fn_ov006_021ff628();
    ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f5870);
    do {
        native_fn_ov006_02203cf0();
        M2C_FIELD(native_data_ov006_0221c06c, u32 (**)(void), 0xC)();
        native_fn_ov006_022048a8(0);
        native_fn_ov006_02204150();
        native_fn_ov006_022047ac();
        native_fn_02008070();
    } while (M2C_FIELD(native_data_ov006_0221c06c, u8 *, 1) == 0);
    native_fn_ov006_021f527c();
    native_fn_02097470(temp_r6);
    return 0U;
}
