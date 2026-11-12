#include "context.h"
u32 native_ov001_021dff00(void) {
    void *temp_r0;

    if (native_data_ov001_022388ec.field_2c == 0x0) {
        if (native_data_ov001_022388ec.field_80 == 0) {
            native_data_ov001_022388ec.field_8 = 0x1B;
        } else {
            native_fn_0202ac08(native_data_ov001_02238988);
            native_fn_ov001_021eea10(0x5C, 0);
            native_data_ov001_022388ec.field_2c = 5;
        }
    }
    else if (native_data_ov001_022388ec.field_2c == 0x5) {
        native_fn_ov001_021d7e80((void *) *(native_data_ov001_0223896c + (native_data_ov001_022388ec.field_2b)));
        native_data_ov001_022388ec.field_2a = (u8) ov001_effect_resource_create_021eec7c(0x5C, (u8 *) *(native_data_ov001_0223896c + (native_data_ov001_022388ec.field_2b)), (s8) native_fn_0205d790(0x5C));
        native_data_ov001_022388ec.field_2c = 6;
    }
    else if (native_data_ov001_022388ec.field_2c == 0x6) {
        if (native_fn_0205d6f4(native_data_ov001_022388ec.field_2a) == 0) {
            native_data_ov001_022388ec.field_2c = 8;
        }
    }
    else if (native_data_ov001_022388ec.field_2c == 0x8) {
        native_fn_ov001_021dc230(*(native_data_ov001_0223896c + (native_data_ov001_022388ec.field_2b)), 1);
        native_fn_ov001_021db788(*(native_data_ov001_0223896c + (native_data_ov001_022388ec.field_2b)), 0);
        native_data_ov001_022388ec.field_2c = 0xA;
    }
    else if (native_data_ov001_022388ec.field_2c == 0xA) {
        temp_r0 = (void *) *(native_data_ov001_0223896c + (native_data_ov001_022388ec.field_2b));
        if (native_fn_ov001_021dbb9c((u32)temp_r0, M2C_FIELD(temp_r0, u8 *, 0x31E)) != 0) {
            native_data_ov001_022388ec.field_2c = 0x64;
        }
    }
    else if (native_data_ov001_022388ec.field_2c == 0x64) {
        native_data_ov001_022388ec.field_2b = (s8) (native_data_ov001_022388ec.field_2b + 1);
        if (*(native_data_ov001_0223896c + (native_data_ov001_022388ec.field_2b)) != 0) {
            native_data_ov001_022388ec.field_2c = 5;
        } else {
            native_fn_0205d718(native_data_ov001_022388ec.field_2a);
            native_fn_ov001_021eeb70(0x5C);
            native_fn_0202ac4c(native_data_ov001_02238988);
            native_data_ov001_022388ec.field_2c = 0;
            native_data_ov001_022388ec.field_2b = 0;
            native_data_ov001_022388ec.field_8 = 0x1B;
        }
    }

    return 0U;
}
