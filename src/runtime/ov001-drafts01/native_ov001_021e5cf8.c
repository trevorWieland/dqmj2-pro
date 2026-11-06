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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u32 native_fn_02041814();
extern u32 native_fn_020418e8();
extern u32 native_fn_02041930();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d7d58();
extern u32 native_fn_ov001_021d7dc4();
extern u32 native_fn_ov001_022139e8();
extern u32 native_fn_ov001_02213b5c();
typedef struct {
    u8 unknown_0[0x11];
    u8 field_11;
    u8 unknown_12[0x4];
    s8 field_16;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e5cf8(void) {
    if (native_data_ov001_02238cd4.field_11 == 0) {
        native_fn_ov001_021d75d4(0x2E);
        native_fn_ov001_021d7d58(0x2E, 0);
        native_fn_ov001_021d7dc4(0x2E, 0);
        native_data_ov001_02238cd4.field_11 = 0xAU;
    }
    if (native_data_ov001_02238cd4.field_11 == 0xA) {
        native_fn_02041510(1, 2, 0x1E);
        native_fn_020418e8(0x1E, 0 - native_fn_02041930());
        native_fn_ov001_022139e8(2);
        native_data_ov001_02238cd4.field_11 = 0xFU;
    }
    if ((native_data_ov001_02238cd4.field_11 == 0xF) && (native_fn_ov001_02213b5c() != 0)) {
        native_data_ov001_02238cd4.field_11 = 0x14U;
    }
    if ((native_data_ov001_02238cd4.field_11 == 0x14) && (native_fn_02041800() != 1) && (native_fn_02041814() != 1)) {
        native_data_ov001_02238cd4.field_11 = 0x64U;
    }
    if (native_data_ov001_02238cd4.field_11 == 0x64) {
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_11 = 0U;
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
