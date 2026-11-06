#include "context.h"
u32 native_ov005_021e6704(void *arg0, void *arg1) {
    s16 temp_r0_2;
    s16 temp_r0_3;
    s16 temp_r0_4;
    s16 temp_r0_5;
    s16 temp_r0_6;
    s16 temp_r0_7;
    s32 temp_r2_2;
    s32 temp_r2_3;
    u32 temp_r5;
    f32 temp_r6;
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;
    s8 var_r0;
    u32 temp_r0_8;
    u8 temp_r0;
    void *temp_r3;
    void *var_r7;
    void *var_r8;
    void *var_r9;

    native_fn_020cf620(1);
    native_fn_02008c58(0, arg1, 4);
    native_fn_02008e0c(arg0, arg1 + 0xA8, 6);
    M2C_FIELD(arg1, u8 *, 0xAE) = (u8) M2C_FIELD(arg0, u8 *, 6);
    M2C_FIELD(arg1, u8 *, 0xAF) = (u8) M2C_FIELD(arg0, u8 *, 7);
    native_fn_02008e0c(arg0 + 8, arg1 + 0xB0, 0x14);
    native_fn_02008e0c(arg0 + 8, arg1, 0x14);
    var_r4 = 0;
    var_r7 = arg1 + 0xC4;
    var_r8 = arg0 + 0x1C;
    do {
        native_fn_02008e0c(var_r8, var_r7, 0x14);
        M2C_FIELD(var_r7, s32 *, 0x14) = (s32) M2C_FIELD(var_r8, s32 *, 0x14);
        M2C_FIELD(var_r7, s16 *, 0x18) = (s16) M2C_FIELD(var_r8, s16 *, 0x18);
        M2C_FIELD(var_r7, u8 *, 0x1B) = (u8) M2C_FIELD(var_r8, u8 *, 0x1A);
        M2C_FIELD(var_r7, u8 *, 0x1E) = (u8) M2C_FIELD(var_r8, u8 *, 0x1B);
        M2C_FIELD(var_r7, u8 *, 0x1C) = (u8) M2C_FIELD(var_r8, u8 *, 0x1B);
        if (M2C_FIELD(var_r8, u8 *, 0x1C) != 0) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        M2C_FIELD(var_r7, s8 *, 0x1D) = var_r0;
        var_r6 = 0;
        M2C_FIELD(var_r7, u8 *, 0x30) = (u8) M2C_FIELD(var_r8, u8 *, 0x30);
        M2C_FIELD(var_r7, u8 *, 0x32) = (u8) M2C_FIELD(var_r8, u8 *, 0x31);
        M2C_FIELD(var_r7, u8 *, 0x33) = (u8) M2C_FIELD(var_r8, u8 *, 0x32);
        M2C_FIELD(var_r7, u8 *, 0x31) = (u8) M2C_FIELD(var_r8, u8 *, 0x33);
        native_fn_ov005_021e6aec(var_r7);
        var_r9 = var_r7 + 0x7A;
        var_r5 = 0;
loop_5:
        temp_r3 = var_r8 + (var_r5 * 4);
        ((NativePair *)((u8 *)var_r7 + 0x7A))[var_r5].first = (u8) M2C_FIELD(temp_r3, u8 *, 0x78);
        ((NativePair *)((u8 *)var_r7 + 0x7A))[var_r5].second = (s8) M2C_FIELD(temp_r3, u16 *, 0x7A);
        native_fn_ov005_021e6b20(var_r9);
        temp_r0 = ((NativePair *)((u8 *)var_r7 + 0x7A))[var_r5].first;
        var_r5 += 1;
        var_r9 += 2;
        if (temp_r0 != 0) {
            var_r6 += 1;
        }
        if (var_r5 < 5) {
            goto loop_5;
        }
        native_fn_0206485c(var_r7 + 0x7A, 5);
        M2C_FIELD(var_r7, s16 *, 0x3C) = (s16) native_fn_ov005_021e6678(M2C_FIELD(var_r7, u8 *, 0x30), var_r6, 1);
        temp_r6 = native_fn_02025578((native_fn_02024e0c(2.0f, (native_fn_02025a70((u32) M2C_FIELD(var_r7, u8 *, 0x1A))))), 2.0f);
        temp_r5 = native_fn_020449d4(M2C_FIELD(var_r7, s16 *, 0x18));
        M2C_FIELD(var_r7, s16 *, 0x20) = (s16) M2C_FIELD(var_r8, s16 *, 0x20);
        M2C_FIELD(var_r7, s16 *, 0x22) = (s16) M2C_FIELD(var_r8, s16 *, 0x22);
        M2C_FIELD(var_r7, s16 *, 0x28) = (s16) M2C_FIELD(var_r8, s16 *, 0x28);
        M2C_FIELD(var_r7, s16 *, 0x2A) = (s16) M2C_FIELD(var_r8, s16 *, 0x2A);
        M2C_FIELD(var_r7, s16 *, 0x2C) = (s16) M2C_FIELD(var_r8, s16 *, 0x2C);
        M2C_FIELD(var_r7, s16 *, 0x2E) = (s16) M2C_FIELD(var_r8, s16 *, 0x2E);
        temp_r0_2 = (s16) native_fn_020259b4((native_fn_02025ab8((native_fn_02025a70((u32) M2C_FIELD(temp_r5, u16 *, 0x10))), temp_r6)));
        if ((s32) M2C_FIELD(var_r7, s16 *, 0x20) > (s32) temp_r0_2) {
            M2C_FIELD(var_r7, s16 *, 0x20) = temp_r0_2;
        }
        temp_r0_3 = (s16) native_fn_020259b4((native_fn_02025ab8((native_fn_02025a70((u32) M2C_FIELD(temp_r5, u16 *, 0x12))), temp_r6)));
        if ((s32) M2C_FIELD(var_r7, s16 *, 0x22) > (s32) temp_r0_3) {
            M2C_FIELD(var_r7, s16 *, 0x22) = temp_r0_3;
        }
        temp_r0_4 = (s16) native_fn_020259b4((native_fn_02025ab8((native_fn_02025a70((u32) M2C_FIELD(temp_r5, u16 *, 0x14))), temp_r6)));
        if ((s32) M2C_FIELD(var_r7, s16 *, 0x28) > (s32) temp_r0_4) {
            M2C_FIELD(var_r7, s16 *, 0x28) = temp_r0_4;
        }
        temp_r0_5 = (s16) native_fn_020259b4((native_fn_02025ab8((native_fn_02025a70((u32) M2C_FIELD(temp_r5, u16 *, 0x16))), temp_r6)));
        if ((s32) M2C_FIELD(var_r7, s16 *, 0x2A) > (s32) temp_r0_5) {
            M2C_FIELD(var_r7, s16 *, 0x2A) = temp_r0_5;
        }
        temp_r0_6 = (s16) native_fn_020259b4((native_fn_02025ab8((native_fn_02025a70((u32) M2C_FIELD(temp_r5, u16 *, 0x18))), temp_r6)));
        if ((s32) M2C_FIELD(var_r7, s16 *, 0x2C) > (s32) temp_r0_6) {
            M2C_FIELD(var_r7, s16 *, 0x2C) = temp_r0_6;
        }
        temp_r0_7 = (s16) native_fn_020259b4((native_fn_02025ab8((native_fn_02025a70((u32) M2C_FIELD(temp_r5, u16 *, 0x1A))), temp_r6)));
        if ((s32) M2C_FIELD(var_r7, s16 *, 0x2E) > (s32) temp_r0_7) {
            M2C_FIELD(var_r7, s16 *, 0x2E) = temp_r0_7;
        }
        M2C_FIELD(var_r7, s16 *, 0x24) = (s16) M2C_FIELD(var_r7, s16 *, 0x20);
        M2C_FIELD(var_r7, s16 *, 0x26) = (s16) M2C_FIELD(var_r7, s16 *, 0x22);
        temp_r0_8 = native_fn_ov005_021e65ec(M2C_FIELD(var_r7, s16 *, 0x18), M2C_FIELD(var_r7, u8 *, 0x1A), 1);
        M2C_FIELD(var_r7, u32 *, 0x34) = native_fn_ov005_021e664c(temp_r0_8, M2C_FIELD(var_r7, u8 *, 0x30));
        M2C_FIELD(var_r7, u32 *, 0x38) = native_fn_ov005_021e664c(temp_r0_8, M2C_FIELD(var_r7, u8 *, 0x30) + 1);
        native_fn_ov005_021e6660(temp_r0_8, 1);
        native_fn_02008d78(var_r7 + 0x40, 0, 0x3A);
        var_r7 += 0x84;
        var_r8 += 0x98;
        var_r4 += 1;
    } while (var_r4 < 3);
    M2C_FIELD(arg1, u16 *, 0x254) = (u16) M2C_FIELD(arg0, u16 *, 0x1E4);
    M2C_FIELD(arg1, u16 *, 0x256) = (u16) M2C_FIELD(arg0, u16 *, 0x1E6);
    M2C_FIELD(arg1, u16 *, 0x258) = (u16) M2C_FIELD(arg0, u16 *, 0x1E8);
    M2C_FIELD(arg1, u8 *, 0x25A) = (u8) M2C_FIELD(arg0, u8 *, 0x1EA);
    M2C_FIELD(arg1, u8 *, 0x25B) = (u8) M2C_FIELD(arg0, u8 *, 0x1EB);
    M2C_FIELD(arg1, s32 *, 0x25C) = (s32) M2C_FIELD(arg0, s32 *, 0x1EC);
    M2C_FIELD(arg1, u16 *, 0x260) = (u16) M2C_FIELD(arg0, u16 *, 0x1F0);
    temp_r2_2 = (M2C_FIELD(arg1, s32 *, 0x14) & ~0xFFF) | (M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x4C) & (-0x1000U >> 0x14));
    M2C_FIELD(arg1, s32 *, 0x14) = temp_r2_2;
    temp_r2_3 = (temp_r2_2 & ~0xF000) | (u16) ((u32) M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x50) << 0xC);
    M2C_FIELD(arg1, s32 *, 0x14) = temp_r2_3;
    M2C_FIELD(arg1, s32 *, 0x14) = (s32) ((temp_r2_3 & ~0x1F0000) | (((u32) M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x54) << 0x1B) >> 0xB));
    M2C_FIELD(arg1, s8 *, 0x262) = 0;
    M2C_FIELD(arg1, s16 *, 0x264) = 0;
    M2C_FIELD(arg1, s16 *, 0x266) = (s16) native_fn_ov005_021e1014(arg1);
    M2C_FIELD(arg1, s32 *, 0x250) = (s32) (M2C_FIELD(arg0, u16 *, 0x1E8) + (M2C_FIELD(arg0, u16 *, 0x1E6) + M2C_FIELD(arg0, u16 *, 0x1E4)));
    M2C_FIELD(arg1, u16 *, 0x256) = (u16) M2C_FIELD(arg0, u16 *, 0x1E6);
    return native_fn_020cf658();
}
