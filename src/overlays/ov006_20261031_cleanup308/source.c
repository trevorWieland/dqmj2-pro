#include "context.h"
u32 native_ov006_021dec9c(void) {
    void *record;
    s32 var_r4;
    u32 temp_r4;

    var_r4 = 4;
    do {
        record=(void *)native_fn_02049ad0(var_r4);
        if (*(s32 *)record != 0) {
            native_fn_02049898(record);
        }
        var_r4 = (s32) (s8) (var_r4 + 1);
    } while (var_r4 <= 0x1C);
    temp_r4 = native_fn_02048f6c(1);
    return native_fn_ov006_021ddf08((s8) temp_r4, native_fn_ov006_021ddf18((s8) native_fn_02048f6c(1)));
}
