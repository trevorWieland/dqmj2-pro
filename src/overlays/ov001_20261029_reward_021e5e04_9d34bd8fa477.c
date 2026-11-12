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
extern u32 native_fn_02041510(u32, u32, u32);
extern u32 native_fn_02041800();
extern u32 native_fn_02041814();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_ov001_021d75d4(u32);
extern u32 native_fn_ov001_021d7d58();
extern u32 native_fn_ov001_021d7dc4();
extern u32 native_fn_ov001_021db578();
extern u32 native_fn_ov001_021db8b8();
extern u32 ov001_begin_state_transition_021f1354(u32, u32, u32, u32);
extern u32 ov001_select_mode_id_021f1438();
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_022139e8(u32);
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0xc];
    u8 field_f;
    u8 field_10;
    u8 unknown_11[0x5];
    s8 field_16;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e5e04(s32 arg0) {
    u8 temp_r2;

    if (native_data_ov001_02238cd4.field_10 == 0) {
        native_fn_ov001_021d75d4(0x2EU);
        native_fn_ov001_021d7d58(0x2E, 0);
        native_fn_ov001_021d7dc4(0x2E, 0);
        if (arg0 != 0) {
            ov001_begin_state_transition_021f1354(1U, 0U, 0x11U, 0U);
            if ((native_fn_ov001_021db8b8(0) != 0) && ((s32) native_fn_ov001_021db578(2) > 0)) {
                ov001_select_mode_id_021f1438(0);
            } else {
                ov001_select_mode_id_021f1438(1);
            }
            native_data_ov001_02238cd4.field_f = 0U;
            native_data_ov001_02238cd4.field_10 = 5U;
        } else {
            native_data_ov001_02238cd4.field_10 = 0xAU;
        }
    }
    if (native_data_ov001_02238cd4.field_10 == 5) {
        if ((u32) ++native_data_ov001_02238cd4.field_f > 0x3CU) {
            ov001_clear_state_flag4_021f14a4();
            native_data_ov001_02238cd4.field_10 = 0xAU;
        }
    }
    if (native_data_ov001_02238cd4.field_10 == 0xA) {
        native_fn_02041510(1U, 2U, 0xFU);
        native_fn_ov001_022139e8(1U);
        native_data_ov001_02238cd4.field_10 = 0x14U;
    }
    if ((native_data_ov001_02238cd4.field_10 == 0x14) && (native_fn_02041800() != 1) && (native_fn_02041814() != 1)) {
        native_data_ov001_02238cd4.field_10 = 0x64U;
    }
    if (native_data_ov001_02238cd4.field_10 == 0x64) {
        native_data_ov001_02238cd4.field_2 = 6;
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_10 = 0U;
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
