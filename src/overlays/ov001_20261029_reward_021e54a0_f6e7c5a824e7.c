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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov001_021d75d4(u32);
extern u32 native_fn_ov001_021d94cc(u32, u32);
extern u32 native_fn_ov001_021dc8e8();
extern u32 native_fn_ov001_021e3564();
extern u32 ov001_begin_state_transition_021f1354(u32, u32, u32, u32);
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_022023c4();
extern u32 native_fn_ov001_02202654();
extern u32 native_fn_ov001_02212858();
typedef struct {
    u8 unknown_0[0xa];
    u8 field_a;
    u8 unknown_b[0xb];
    s8 field_16;
    u8 unknown_17[0x2];
    s8 field_19;
    u8 unknown_1a[0x1];
    s8 field_1b;
    s8 field_1c;
    u8 unknown_1d[0x2];
    s8 field_1f;
    u8 field_20;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e54a0(void) {
    u32 temp_r4;

    temp_r4 = native_fn_0202a634();
    if (native_data_ov001_02238cd4.field_20 == 0) {
        native_fn_ov001_021d75d4(0x2AU);
        native_fn_ov001_021d94cc(1U, 0U);
        native_fn_ov001_021e3564(0x14, 1);
        native_fn_ov001_02202654();
        native_fn_ov001_021dc8e8(0);
        native_data_ov001_02238cd4.field_1f = 0;
        native_data_ov001_02238cd4.field_20 = 1U;
    }
    if (native_data_ov001_02238cd4.field_20 == 1) {
        if (native_data_ov001_02238cd4.field_a != 0) {
            native_data_ov001_02238cd4.field_1c = (s8) native_fn_0205e7a8(-1, 0x3A);
            native_data_ov001_02238cd4.field_1b = 0x14;
            native_data_ov001_02238cd4.field_20 = 3U;
            native_data_ov001_02238cd4.field_19 = 0x12;
            ov001_begin_state_transition_021f1354(1U, 0U, 0xBU, 1U);
            native_fn_ov001_02212858(native_data_ov001_02238cd4.field_1c);
        }
    } else if (native_data_ov001_02238cd4.field_20 == 3) {
        if (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7) {
            ov001_clear_state_flag4_021f14a4();
            native_data_ov001_02238cd4.field_20 = 2U;
        }
    } else if (native_data_ov001_02238cd4.field_20 == 2) {
        if ((s32) native_data_ov001_02238cd4.field_19 <= 0) {
            native_fn_02041510(1U, 2U, 0x1EU);
            native_data_ov001_02238cd4.field_20 = 0xCU;
            native_fn_ov001_022023c4(0x400);
        }
    } else if (native_data_ov001_02238cd4.field_20 == 12) {
        if (native_fn_02041800() != 1) {
            native_data_ov001_02238cd4.field_20 = 0x13U;
        }
    }
    if (native_data_ov001_02238cd4.field_20 == 0x13) {
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_20 = 0U;
    }
    if ((s32) native_data_ov001_02238cd4.field_19 > 0) {
        native_data_ov001_02238cd4.field_19 = (s8) (native_data_ov001_02238cd4.field_19 - 1);
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
