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
extern u32 native_fn_ov001_021d80c0();
extern u32 native_fn_ov001_021d94cc(u32, u32);
extern u32 native_fn_ov001_021dc8e8();
extern u32 native_fn_ov001_021e3564();
extern u32 native_fn_ov001_021e3b34();
extern u32 native_fn_ov001_021e3bd0();
extern u32 native_fn_ov001_021e3be4();
extern u32 native_fn_ov001_021f1354(u32, u32, u32, u32);
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f1a44();
extern u32 native_fn_ov001_02202654();
extern u32 native_fn_ov001_02212858();
extern u32 native_fn_ov001_022139e8(u32);
typedef struct {
    u8 unknown_0[0x6];
    s8 field_6;
    s8 field_7;
    s8 field_8;
    u8 field_9;
    u8 field_a;
    u8 unknown_b[0xb];
    s8 field_16;
    u8 unknown_17[0x11];
    s16 field_28;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e634c(void) {
    u32 temp_r4;

    temp_r4 = native_fn_0202a634();
    if (native_data_ov001_02238cd4.field_9 == 0) {
        native_fn_ov001_021e3b34();
        native_fn_ov001_021d75d4(0x2AU);
        native_fn_ov001_021d94cc(1U, 0U);
        native_fn_ov001_021e3564(0x14, 1);
        native_fn_ov001_02202654();
        native_fn_ov001_021dc8e8(0);
        native_fn_ov001_021dc8e8(2);
        native_data_ov001_02238cd4.field_9 = 1U;
    }
    if (native_data_ov001_02238cd4.field_9 == 1) {
        if (native_data_ov001_02238cd4.field_a != 0) {
            native_data_ov001_02238cd4.field_8 = (s8) native_fn_ov001_021e3be4();
            native_data_ov001_02238cd4.field_7 = (s8) native_fn_0205e7a8(-1, 0x3A);
            native_fn_ov001_021f1354(1U, 0U, 0xBU, 1U);
            native_data_ov001_02238cd4.field_9 = 0xFU;
            native_data_ov001_02238cd4.field_6 = 0x12;
            native_data_ov001_02238cd4.field_28 = 0xB4;
            native_fn_ov001_02212858(native_data_ov001_02238cd4.field_7);
        }
    } else if (native_data_ov001_02238cd4.field_9 == 15) {
        if (native_data_ov001_02238cd4.field_6 == 0) {
            if ((native_data_ov001_02238cd4.field_28 == 0) || (M2C_FIELD(temp_r4, u16 *, 2) & 0xFF7)) {
                native_data_ov001_02238cd4.field_9 = 0x10U;
                native_fn_ov001_021f14a4();
                native_fn_ov001_021d75d4(0x2EU);
            }
        }
    }
    if ((native_data_ov001_02238cd4.field_9 == 0x10) && (native_fn_ov001_021d80c0() != 0)) {
        native_fn_ov001_022139e8(2U);
        native_fn_02041510(1U, 2U, 0x1EU);
        native_data_ov001_02238cd4.field_9 = 0x11U;
    }
    if ((native_data_ov001_02238cd4.field_9 == 0x11) && (native_fn_02041800() != 1)) {
        native_data_ov001_02238cd4.field_9 = 0x12U;
        M2C_FIELD((void *) native_fn_ov001_021f1a44(native_data_ov001_02238cd4.field_8), s8 *, 0x23) = 0;
    }
    if ((native_data_ov001_02238cd4.field_9 == 0x12) && (M2C_FIELD((void *) native_fn_ov001_021f1a44(native_data_ov001_02238cd4.field_8), s32 *, 0x1C) == 0)) {
        native_data_ov001_02238cd4.field_9 = 0x13U;
    }
    if (native_data_ov001_02238cd4.field_9 == 0x13) {
        native_fn_ov001_021e3bd0();
        native_data_ov001_02238cd4.field_16 = 0xF;
        native_data_ov001_02238cd4.field_9 = 0U;
    }
    if ((s32) native_data_ov001_02238cd4.field_6 > 0) {
        native_data_ov001_02238cd4.field_6 = (s8) (native_data_ov001_02238cd4.field_6 - 1);
    }
    if ((s32) native_data_ov001_02238cd4.field_28 > 0) {
        native_data_ov001_02238cd4.field_28 = (s16) (native_data_ov001_02238cd4.field_28 - 1);
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
