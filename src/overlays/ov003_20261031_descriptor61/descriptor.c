#include "context.h"
u32 native_ov003_021deaf8(s32 *arg0) {
    void *temp_r2;
    u32 temp_r4;

    temp_r4 = native_fn_02049f24();
    native_fn_02049f30();
    temp_r2 = M2C_FIELD(*(void **) native_fn_02049ad0((s8) ((u32)*arg0 + 8U)), void **, 4);
    native_fn_02046af4(native_data_021c9698, M2C_FIELD(temp_r2, s32 *, 0x68), M2C_FIELD(temp_r2, u8 *, 0x5E), 0, temp_r4, 0xFF);
    return native_fn_02049f14(temp_r4);
}
