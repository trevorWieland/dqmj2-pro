typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
extern u32 native_fn_02041510(u32, u32, u32);
extern u32 native_fn_02041800();
extern u32 native_fn_02041898(u32);
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_02048094(u32, u32);
extern u32 native_fn_ov001_021d75d4(u32);
extern u32 native_fn_ov001_021d774c(u32);
extern u32 native_fn_ov001_021d94cc(u32, u32);
extern u32 native_fn_ov001_021e3508(u32);
extern u32 native_fn_ov001_021f1294(u32, u32);
extern u32 native_fn_ov001_021f1324();
extern u32 ov001_begin_state_transition_021f1354(u32, u32, u32, u32);
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_021f949c(u32, u32);
extern u32 native_fn_ov001_022139e8(u32);
typedef struct {
    u8 unknown_0[0x12];
    u8 field_12;
    u8 field_13;
    u8 unknown_14[0x2];
    s8 field_16;
    u8 unknown_17[0x15];
    s32 field_2c;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e5ac8(void) {
    u8 temp_r2;
    u8 temp_r2_2;

    if (native_data_ov001_02238cd4.field_13 == 0) {
        ov001_begin_state_transition_021f1354(1, 0, 2, 0);
        native_fn_ov001_021d75d4(0x2A);
        native_fn_ov001_021d94cc(1, 1);
        native_fn_ov001_021f949c(0xDE, 1);
        native_data_ov001_02238cd4.field_13 = 5U;
    } else if (native_data_ov001_02238cd4.field_13 == 5) {
        native_fn_02041898(0);
        native_data_ov001_02238cd4.field_13 = 0xAU;
    }
    if ((native_data_ov001_02238cd4.field_13 == 0xA) && (native_fn_ov001_021d774c(-1) == 0)) {
        ov001_clear_state_flag4_021f14a4();
        if (native_data_ov001_02238cd4.field_2c == 0) {
            native_fn_02041510(1, 2, 0x1E);
            native_fn_ov001_022139e8(2);
            native_data_ov001_02238cd4.field_13 = 0x14U;
        } else {
            native_data_ov001_02238cd4.field_13 = 0x1EU;
            native_data_ov001_02238cd4.field_12 = 0U;
        }
    }
    if ((native_data_ov001_02238cd4.field_13 == 0x14) && (native_fn_02041800() != 1)) {
        native_data_ov001_02238cd4.field_13 = 0x64U;
    }
    if (native_data_ov001_02238cd4.field_13 == 0x1E) {
        if (native_data_ov001_02238cd4.field_12 == 0) {
            native_fn_ov001_021f1324();
        }
        if ((u32) ++native_data_ov001_02238cd4.field_12 >= 2U) {
            native_fn_ov001_021f1294(0x10, 2);
            native_data_ov001_02238cd4.field_13 = 0x28U;
        }
    }
    if (native_data_ov001_02238cd4.field_13 == 0x28) {
        native_fn_02048094(native_data_ov001_02238cd4.field_2c, 0);
        ov001_begin_state_transition_021f1354(1, 0, 0x16, 0);
        native_fn_ov001_021e3508(0 - native_data_ov001_02238cd4.field_2c);
        native_data_ov001_02238cd4.field_13 = 0x32U;
        native_data_ov001_02238cd4.field_12 = 0U;
    }
    if (native_data_ov001_02238cd4.field_13 == 0x32) {
        if ((u32) ++native_data_ov001_02238cd4.field_12 >= 0x1EU) {
            ov001_clear_state_flag4_021f14a4();
            native_fn_02041510(1, 2, 0x1E);
            native_fn_ov001_022139e8(2);
            native_data_ov001_02238cd4.field_13 = 0x14U;
        }
    }
    if (native_data_ov001_02238cd4.field_13 == 0x64) {
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_13 = 0U;
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
