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
extern u32 native_fn_020443fc();
extern u32 native_fn_02044414();
extern u32 native_fn_02044424();
extern u32 native_fn_ov001_021dfbcc();
extern u32 native_fn_ov001_021dfc58();
typedef struct {
    u8 unknown_0[0x7];
    u8 field_7;
    s8 field_8;
    u8 unknown_9[0x3];
    u8 field_c;
    u8 unknown_d[0x3];
    u8 field_10;
    u8 unknown_11[0xa];
    u8 field_1b;
    u8 unknown_1c[0x1];
    u8 field_1d;
    u8 unknown_1e[0x6];
    u8 field_24;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
extern u8 native_data_ov001_022388ff[];
extern u8 native_data_ov001_02238900[];
extern u8 native_data_ov001_02238901[];
extern u8 native_data_ov001_02238902[];
extern u8 native_data_ov001_02238913[];
u32 native_ov001_021e0328(void) {
    u32 temp_r4;

    native_fn_020443fc();
    if (native_data_ov001_022388ec.field_7 != 0) {
        native_data_ov001_022388ec.field_7 = 0U;
    }
    if (native_data_ov001_022388ec.field_1b != 0) {
        native_data_ov001_022388ec.field_1b = 0U;
    }
    if (native_data_ov001_022388ec.field_c != 0) {
        native_data_ov001_022388ec.field_c = 0U;
    }
    if (native_data_ov001_022388ec.field_1d != 0) {
        native_data_ov001_022388ec.field_1d = 0U;
    }
    native_fn_ov001_021dfbcc(4, native_data_ov001_022388ff, 0x2F, 4);
    native_fn_ov001_021dfbcc(1, native_data_ov001_02238913, 0x2E, 3);
    native_fn_ov001_021dfc58(8, native_data_ov001_02238900, 0x39, 4, 0);
    native_fn_ov001_021dfc58(0x10, native_data_ov001_02238901, 0x39, 4, 1);
    native_fn_ov001_021dfbcc(0x20, native_data_ov001_02238902, 0x38, 4);
    native_data_ov001_022388ec.field_24 = (u8) native_data_ov001_022388ec.field_10;
    temp_r4 = native_fn_02044414();
    if ((native_fn_02044424(0x800000) != 0) && ((s32) temp_r4 >= 5)) {
        native_data_ov001_022388ec.field_8 = 0x32;
    } else if ((native_fn_02044424(0x01000000) != 0) && ((s32) temp_r4 >= 0xA)) {
        native_data_ov001_022388ec.field_8 = 0x32;
    } else {
        native_data_ov001_022388ec.field_8 = 0x34;
    }
    return 1U;
}
