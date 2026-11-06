#include "context.h"
u32 native_ov006_021e2f68(void) {
    s32 *temp_r4;
    s32 *temp_r4_2;

    native_fn_020684ac(3, 0);
    native_fn_020684ac(2, 1);
    if (native_fn_020642dc() == 0x25) {
        native_fn_ov006_021ded5c(0xF, 4, 0x4D);
        return native_fn_ov006_021e2f58(0xC);
    }
    native_fn_ov006_021dff30();
    native_fn_02008d78(native_fn_02063eec(), 0, 0x100);
    native_fn_ov006_021ded5c(0xF, 4, 0x26);
    native_fn_ov006_021def28(1);
    native_fn_ov006_021df590(0x52);
    temp_r4 = native_fn_02063ee0();
    if ((u32) *temp_r4 < (u32) M2C_FIELD((void *) native_fn_02067b58(), u32 *, 0x24)) {
        temp_r4_2 = native_fn_02063ee0();
        *temp_r4_2 = M2C_FIELD((void *) native_fn_02067b58(), s32 *, 0x24);
        native_fn_020684ac(4, 0);
        native_fn_ov006_021df974(3, 0x15, native_data_ov006_02217c18, 0x1100);
        return native_fn_ov006_021e2f58(0xD);
    }
    native_fn_ov006_021df974(3, 0x17, native_data_ov006_02217bf0, 0x10);
    return native_fn_ov006_021e2f58(0);
}
