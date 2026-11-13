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
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_0202a634();
extern u32 native_fn_02041510(u32, u32, u32);
extern u32 native_fn_02041800();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_020443ec();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205f210();
extern u32 native_fn_0205f2d8();
extern u32 native_fn_ov001_021d75d4(u32);
extern u32 native_fn_ov001_021d774c(u32);
extern u32 native_fn_ov001_021d7d58();
extern u32 native_fn_ov001_021d7dc4();
extern u32 native_fn_ov001_021e3564(u32, u32);
extern u32 ov001_begin_state_transition_021f1354(u32, u32, u32, u32);
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_022139e8(u32);
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0x9];
    s8 field_c;
    u8 field_d;
    u8 field_e;
    u8 unknown_f[0x7];
    s8 field_16;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e5f88(s32 arg0) {
    u8 temp_r0;

    if (native_data_ov001_02238cd4.field_e == 0x0) {
        native_fn_ov001_021d75d4(0x2EU);
        native_fn_ov001_021d7d58(0x2E, 0);
        native_fn_ov001_021d7dc4(0x2E, 0);
        native_data_ov001_02238cd4.field_d = 0U;
        native_data_ov001_02238cd4.field_e = 0xAU;
    } else if (native_data_ov001_02238cd4.field_e == 0xA) {
        if (++native_data_ov001_02238cd4.field_d & 0xFF) {
            native_data_ov001_02238cd4.field_e = 0x14U;
        }
    } else if (native_data_ov001_02238cd4.field_e == 0x14) {
        native_fn_ov001_021d75d4(0x2AU);
        if (arg0 == 0xB) {
            native_fn_ov001_021e3564(0x14, 1);
            ov001_begin_state_transition_021f1354(1U, 0U, 0xEU, 1U);
            native_data_ov001_02238cd4.field_c = (s8) native_fn_0205e7a8(-1, 0x3A);
        } else if (arg0 == 0xA) {
            native_fn_ov001_021e3564(0x15, 1);
            ov001_begin_state_transition_021f1354(1U, 0U, 0xFU, 1U);
            native_data_ov001_02238cd4.field_c = (s8) native_fn_0205e7a8(-1, 0x3B);
        } else {
            native_fn_ov001_021e3564(0x15, 1);
            ov001_begin_state_transition_021f1354(1U, 0U, 0x10U, 1U);
            native_data_ov001_02238cd4.field_c = (s8) native_fn_0205e7a8(-1, 0x3A);
        }
        native_data_ov001_02238cd4.field_e = 0x32U;
    } else if (native_data_ov001_02238cd4.field_e == 0x32) {
        if (M2C_FIELD((void *) native_fn_0202a634(), u16 *, 2) & 0xFF7) {
            native_data_ov001_02238cd4.field_e = 0x3CU;
        }
        if (native_fn_ov001_021d774c(-1U) == 0) {
            native_data_ov001_02238cd4.field_e = 0x3CU;
        }
    } else if (native_data_ov001_02238cd4.field_e == 0x3C) {
        if (native_fn_0205f2d8(native_data_ov001_02238cd4.field_c) == 0) {
            native_fn_0205f210(native_data_ov001_02238cd4.field_c, 0x1E);
            native_fn_02041510(1U, 2U, 0x1EU);
            ov001_clear_state_flag4_021f14a4();
            native_fn_ov001_022139e8(2U);
            native_data_ov001_02238cd4.field_e = 0x46U;
        }
    } else if (native_data_ov001_02238cd4.field_e == 0x46) {
        if (native_fn_02041800() != 1) {
            native_data_ov001_02238cd4.field_e = 0x64U;
        }
    }
    if (native_data_ov001_02238cd4.field_e == 0x64) {
        if (arg0 == 0xB) {
            native_data_ov001_02238cd4.field_2 = 0;
        } else if (arg0 != 0xA) {
            native_data_ov001_02238cd4.field_2 = 5;
        } else {
            native_fn_020443ec();
            native_data_ov001_02238cd4.field_2 = 2;
        }
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_e = 0U;
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
