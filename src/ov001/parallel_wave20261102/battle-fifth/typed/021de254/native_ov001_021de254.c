#include "context.h"
u32 native_ov001_021de254(void) {
    s32 temp_r2;
    u32 temp_r4;
    u32 temp_r5;
    u8 temp_r6;

    if ((s8) native_data_ov001_022388ec.field_0 == 0) {
        temp_r6 = *(native_data_ov001_02238a08 + (native_data_ov001_022388ec.field_1c * 8));
        if ((u32) (temp_r6 - 0x2A) <= 1U) {
            native_fn_ov001_02217910(temp_r6);
            if (native_fn_ov001_02216cfc(*(native_data_ov001_02238a0c + (native_data_ov001_022388ec.field_1c * 2)), *(native_data_ov001_02238a08 + (native_data_ov001_022388ec.field_1c * 8))) != 0) {
                native_data_ov001_022388ec.field_0 = 0xA;
            }
        } else {
            switch (temp_r6) {
            case 0x48:
                native_fn_ov001_02217910(temp_r6);
                temp_r5 = native_fn_0207b748(temp_r6);
                if (native_fn_ov001_022170f4(*(native_data_ov001_02238a0c + (native_data_ov001_022388ec.field_1c * 2)), native_fn_0207b6e8(temp_r6), temp_r5) != 0) {
                    native_data_ov001_022388ec.field_0 = 0xA;
                }
                break;
            case 0xED:
            case 0xBE:
                native_fn_ov001_02217910(temp_r6);
                temp_r4 = native_fn_0207b748(temp_r6);
                if (native_fn_ov001_022170f4(*(native_data_ov001_02238a0c + (native_data_ov001_022388ec.field_1c * 2)), native_fn_0207b6e8(temp_r6), temp_r4) != 0) {
                    native_data_ov001_022388ec.field_0 = 0xA;
                }
                break;
            default:
                temp_r2 = *(native_data_ov001_02238a0c + (native_data_ov001_022388ec.field_1c * 2));
                native_data_ov001_022388ec.field_48 = temp_r2;
                native_data_ov001_022388ec.field_40 = temp_r2;
                native_fn_ov001_02217910(temp_r6);
                if (native_fn_ov001_02217920(*(native_data_ov001_02238a08 + (native_data_ov001_022388ec.field_1c * 8))) != 0) {
                    native_data_ov001_022388ec.field_0 = 0xA;
                }
                break;
            }
        }
    } else if ((s8) native_data_ov001_022388ec.field_0 == 0xA) {
        native_data_ov001_022388ec.field_1c = (s8) (native_data_ov001_022388ec.field_1c + 1);
        if (*(native_data_ov001_02238a08 + (native_data_ov001_022388ec.field_1c * 8)) == 0) {
            native_data_ov001_022388ec.field_8 = 0x2A;
            native_data_ov001_022388ec.field_4 = 1;
        }
        native_data_ov001_022388ec.field_0 = 0;
    }
    return 0U;
}
