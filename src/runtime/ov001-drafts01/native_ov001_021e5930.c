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
extern u32 native_fn_0202a634();
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_020444ec();
extern u32 native_fn_02044520();
extern u32 native_fn_0204453c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205f210();
extern u32 native_fn_0205f2d8();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d774c();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021e3564();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_022139e8();
typedef struct {
    u8 unknown_0[0x14];
    s8 field_14;
    u8 field_15;
    s8 field_16;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e5930(void) {
    if (native_data_ov001_02238cd4.field_15 == 0) {
        if ((native_fn_020444ec() != 0) || (native_fn_02044520() != 0) || (native_fn_0204453c() != 0)) {
            native_fn_ov001_021f1354(1, 0, 0xC, 0);
        } else {
            native_fn_ov001_021f1354(1, 0, 3, 0);
        }
        native_fn_ov001_021d75d4(0x2A);
        native_fn_ov001_021d94cc(1, 0);
        native_fn_ov001_021e3564(0x15, 1);
        native_data_ov001_02238cd4.field_14 = (s8) native_fn_0205e7a8(-1, 0x3B);
        native_data_ov001_02238cd4.field_15 = 0xAU;
    }
    if (native_data_ov001_02238cd4.field_15 == 0xA) {
        if (native_fn_ov001_021d774c(-1) == 0) {
            native_data_ov001_02238cd4.field_15 = 0x14U;
        }
        if (M2C_FIELD((void *) native_fn_0202a634(), u16 *, 2) & 0xFF7) {
            native_data_ov001_02238cd4.field_15 = 0x14U;
        }
    }
    if ((native_data_ov001_02238cd4.field_15 == 0x14) && (native_fn_0205f2d8(native_data_ov001_02238cd4.field_14) == 0)) {
        native_fn_02041510(1, 2, 0x1E);
        native_fn_0205f210(native_data_ov001_02238cd4.field_14, 0x1E);
        native_fn_ov001_021f14a4();
        native_fn_ov001_022139e8(2);
        native_data_ov001_02238cd4.field_15 = 0x1EU;
    }
    if ((native_data_ov001_02238cd4.field_15 == 0x1E) && (native_fn_02041800() != 1)) {
        native_data_ov001_02238cd4.field_15 = 0x64U;
    }
    if (native_data_ov001_02238cd4.field_15 == 0x64) {
        native_data_ov001_02238cd4.field_16 = 0x11;
        native_data_ov001_02238cd4.field_15 = 0U;
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
