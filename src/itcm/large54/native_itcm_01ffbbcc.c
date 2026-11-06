#include "context.h"
u32 native_itcm_01ffbbcc(void) {
    struct { struct {u16 x,y;} second,first;u16 text[32]; } frame;
    s32 temp_r4;
    s32 temp_r8;
    s32 var_r10;
    s32 temp_r0;
    s32 temp_r0_4;
    s32 var_r5;
    s8 var_r5_2;
    s32 var_r7;
    u32 temp_r0_3;
    u32 temp_r0_6;
    u32 temp_r5;
    u32 temp_r9;
    u32 temp_r9_2;
    u32 temp_r9_3;
    u8 *temp_r0_5;
    u8 *temp_r4_3;
    u8 *temp_r8_2;
    u8 *temp_r8_3;
    u8 *temp_r8_4;
    u8 *var_r6;
    u8 temp_r0_2;
    void *temp_r4_2;

    frame.first.y = M2C_FIELD(native_data_020dc88c, u16 *, 6);
    frame.first.x = M2C_FIELD(native_data_020dc88c, u16 *, 4);
    if (M2C_FIELD(native_data_021d4100, s32 *, 0x10) == 0x2B) {
        return (u32) M2C_FIELD(native_data_021d4100, s32 *, 0x10);
    }
    var_r5 = 0;
    if ((s32) M2C_FIELD(native_fn_01ffb340(), u16 *, 0xC) > 0) {
        do {
            native_fn_02049ad0((s8) (var_r5 + 5));
            native_fn_02049f4c();
            temp_r0 = var_r5 + 1;
            temp_r4 = (s32)((u32)temp_r0 << 24);
            var_r5 = temp_r4 >> 0x18;
        } while ((s32) M2C_FIELD(native_fn_01ffb340(), u16 *, 0xC) > (s32) (temp_r4 >> 0x18));
    }
    var_r10 = 1;
    var_r7 = 0;
    if ((s32) M2C_FIELD(native_fn_01ffb340(), u16 *, 0xC) > 0) {
        var_r6 = native_data_021d41f4;
        do {
            switch (M2C_FIELD(native_data_021d4100, s32 *, 0x10)) {
            case 42:
        if ((s8) *var_r6 != -1) {
                    native_fn_02046af4(native_data_021c9698, native_fn_020685f0(), 0x1F, 0, frame.text, 0xFF);
                    temp_r0_2 = native_data_021d41fc[(s8) *var_r6];
                    switch (temp_r0_2) {
                    case 1:
                        native_fn_0204a808((s8) (var_r7 + 5), &frame.first, 1, frame.text, 1);
                        break;
                    case 2:
                        native_fn_0204a808((s8) (var_r7 + 5), &frame.first, 5, frame.text, 1);
                        break;
                    case 3:
                        native_fn_0204a808((s8) (var_r7 + 5), &frame.first, 3, frame.text, 1);
                        break;
                    }
                } else {
                    temp_r9_2 = native_fn_01ffa978();
                    temp_r8_3 = native_fn_01ffb334();
                    native_fn_0204a574((s8) (var_r7 + 5), &frame.first, temp_r9_2, *temp_r8_3, (s32) M2C_FIELD(native_fn_01ffb334(), u16 *, 2), 3, 1);
                    }
                break;
            case 10:
            case 11:
                        if ((native_fn_02063b40(0x11D) == 0) && ((var_r7 + 5) == 6)) {
                            var_r10 = 3;
                        }
                        temp_r9 = native_fn_01ffa978();
                        temp_r8_2 = native_fn_01ffb334();
                        native_fn_0204a574((s8) (var_r7 + 5), &frame.first, temp_r9, *temp_r8_2, (s32) (u16) (var_r7 + M2C_FIELD(native_fn_01ffb334(), s16 *, 2)), var_r10, 1);
                break;
            case 43:
            case 45:
            case 46:
            case 48:
                break;
            default:
                    temp_r9_3 = native_fn_01ffa978();
                    temp_r8_4 = native_fn_01ffb334();
                    native_fn_0204a574((s8) (var_r7 + 5), &frame.first, temp_r9_3, *temp_r8_4, (s32) (u16) (var_r7 + M2C_FIELD(native_fn_01ffb334(), s16 *, 2)), 1, 1);
                break;
            }
            var_r6 += 1;
            temp_r0_4 = var_r7 + 1;
            temp_r8 = (s32)((u32)temp_r0_4 << 24);
            var_r7 = temp_r8 >> 0x18;
        } while ((s32) M2C_FIELD(native_fn_01ffb340(), u16 *, 0xC) > (s32) (temp_r8 >> 0x18));
    }
    var_r5_2 = 0;
    do {
        temp_r0_5 = native_fn_02049ad0(var_r5_2);
        if (M2C_FIELD(temp_r0_5, void **, 0) != NULL) {
            temp_r0_6 = native_fn_ov000_022238c0(M2C_FIELD(temp_r0_5, s8 *, 5));
            if (temp_r0_6 != 0x7F) {
                temp_r4_2 = M2C_FIELD(M2C_FIELD(temp_r0_5, void **, 0), void **, 4);
                native_fn_0206006c(native_fn_ov000_02223c40((s8) temp_r0_6), M2C_FIELD(temp_r4_2, s8 *, 0x1C), M2C_FIELD(temp_r4_2, s8 *, 0x1D), M2C_FIELD(temp_r4_2, s8 *, 0x1E), (s32) M2C_FIELD(temp_r4_2, s8 *, 0x1F));
            }
        }
        var_r5_2 += 1;
    } while ((s32) var_r5_2 < 0x1F);
    frame.second.y = M2C_FIELD(native_data_020dc88c, u16 *, 2);
    frame.second.x = M2C_FIELD(native_data_020dc88c, u16 *, 0);
    if (M2C_FIELD(native_fn_01ffb334(), s16 *, 4) != -1) {
        temp_r5 = native_fn_01ffa978();
        temp_r4_3 = native_fn_01ffb334();
        native_fn_0204a574(0, &frame.second, temp_r5, (u8) M2C_FIELD(temp_r4_3, s16 *, 4), (s32) M2C_FIELD(native_fn_01ffb334(), u16 *, 6), 1, 1);
    }
    return native_fn_02049604(native_fn_01ffb340(), 0);
}
