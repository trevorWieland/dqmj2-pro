#include "context.h"
void native_ov000_02219494(void) {
    NativeVector sp0;
    s32 temp_r0;
    s32 temp_r0_2;
    s32 temp_r0_3;
    s32 temp_r0_4;
    u32 temp_r0_6;
    u32 temp_r0_7;
    u32 temp_r0_8;
    u32 temp_r4;
    u32 temp_r5;
    u8 temp_r0_11;
    u8 temp_r0_5;
    u8 temp_r0_9;
    void *temp_r0_10;

    temp_r4 = native_fn_02066c3c();
    temp_r5 = native_fn_0202a634();
    temp_r0_10 = (void *) native_fn_ov000_021df3bc((s32) native_fn_ov000_021df1f0());
    if (M2C_FIELD(temp_r0_10, u8 *, 3) == 0xFF) {
        return;
    }
    if ((u32) M2C_FIELD(temp_r0_10, u8 *, 8) <= 0x20U) {
        temp_r0_9 = M2C_FIELD(temp_r0_10, u8 *, 9);
        if ((u32) temp_r0_9 <= 0x18U) {
            return;
        }
    }
    temp_r0_8 = native_fn_ov000_02218800(3);
    if (temp_r0_8 != 0) {
        return;
    }
    temp_r0_7 = native_fn_ov000_02218800(1);
    if (temp_r0_7 != 0) {
        return;
    }
    temp_r0_6 = native_fn_ov000_02218800(2);
    if (temp_r0_6 != 0) {
        return;
    }
    if ((M2C_FIELD(temp_r4, u8 *, 0) == 1) && (native_fn_020404e0() == 5)) {
        native_data_ov000_02245e54.field1c = (s16) M2C_FIELD(temp_r4, u8 *, 1);
        native_data_ov000_02245e54.field1e = (s16) M2C_FIELD(temp_r4, u8 *, 2);
        native_data_ov000_02245e54.field10 = 0;
        native_data_ov000_02245e54.field12 = 0;
        native_data_ov000_02245e54.field20 = 1;
        native_fn_02041510(1U, 2U, 4U);
        native_fn_02041560(0xA);
        native_fn_020404f0(0x2EU);
        native_fn_ov000_021e7b9c(0x52U);
        native_fn_ov000_0221993c(0U);
        return;
    }
    temp_r0_11 = M2C_FIELD(temp_r4, u8 *, 0);
    if (temp_r0_11 == 1) {
        native_data_ov000_02245e54.field1c = (s16) M2C_FIELD(temp_r4, u8 *, 1);
        native_data_ov000_02245e54.field1e = (s16) M2C_FIELD(temp_r4, u8 *, 2);
        return;
    }
    if ((temp_r0_11 == 3) && (native_data_ov000_02245e54.field20 != 0)) {
        native_data_ov000_02245e54.field10 += (s16) (M2C_FIELD(temp_r4, u8 *, 1) - native_data_ov000_02245e54.field1c);
        native_data_ov000_02245e54.field12 += (s16) (M2C_FIELD(temp_r4, u8 *, 2) - native_data_ov000_02245e54.field1e);
        native_data_ov000_02245e54.field1c = (s16) M2C_FIELD(temp_r4, u8 *, 1);
        temp_r0_5 = M2C_FIELD(temp_r4, u8 *, 2);
        native_data_ov000_02245e54.field1e = (s16) temp_r0_5;
        return;
    }
    if (M2C_FIELD(temp_r5, u16 *, 2) != 0) {
        if (native_data_ov000_02245e54.field20 == 0) {
            return;
        }
        native_data_ov000_02245e54.field10 = 0;
        native_data_ov000_02245e54.field12 = 0;
        native_data_ov000_02245e54.field28 = 1;
        native_data_ov000_02245e54.field20 = 0;
        native_fn_ov000_021e7b9c(0x53U);
        return;
    }
    if (native_data_ov000_02245e54.field28 == 0) {
        return;
    }
    sp0 = native_data_ov000_02245ea0;
    native_fn_ov000_02219ce4(&sp0);
    temp_r0_4 = sp0.x - 0x3000;
    if ((s32) native_data_ov000_02245e54.field40.x < temp_r0_4) {
        return;
    }
    temp_r0_3 = sp0.x + 0x3000;
    if ((s32) native_data_ov000_02245e54.field40.x > temp_r0_3) {
        return;
    }
    temp_r0_2 = sp0.z - 0x3000;
    if ((s32) native_data_ov000_02245e54.field40.z < temp_r0_2) {
        return;
    }
    temp_r0 = sp0.z + 0x3000;
    if ((s32) native_data_ov000_02245e54.field40.z > temp_r0) {
        return;
    }
    native_data_ov000_02245e54.field28 = 0;
    native_fn_020404f0(5U);
    native_fn_ov000_0221993c(1U);
    native_fn_02041510(0U, 2U, 4U);
    native_fn_020418e8(4U, 0xAU);
    return;
}
