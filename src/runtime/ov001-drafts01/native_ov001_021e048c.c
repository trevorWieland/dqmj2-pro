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
extern u32 native_fn_ov001_021dfb30();
extern u32 native_fn_ov001_021dfb94();
typedef struct {
    u8 unknown_0[0x10];
    u8 field_10;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021e048c(void) {
    if (native_data_ov001_022388ec.field_10 & 4) {
        native_fn_ov001_021dfb94(0x2F, -1, 1);
    } else {
        native_fn_ov001_021dfb94(0x2F, -1, 0);
    }
    if (native_data_ov001_022388ec.field_10 & 1) {
        native_fn_ov001_021dfb94(0x2E, -1, 1);
    } else {
        native_fn_ov001_021dfb94(0x2E, -1, 0);
    }
    if (native_data_ov001_022388ec.field_10 & 8) {
        native_fn_ov001_021dfb30(0, 0x39, -1, 1);
    } else {
        native_fn_ov001_021dfb30(0, 0x39, -1, 0);
    }
    if (native_data_ov001_022388ec.field_10 & 0x10) {
        native_fn_ov001_021dfb30(1, 0x39, -1, 1);
    } else {
        native_fn_ov001_021dfb30(1, 0x39, -1, 0);
    }
    if (native_data_ov001_022388ec.field_10 & 0x20) {
        return native_fn_ov001_021dfb94(0x38, -1, 1);
    }
    return native_fn_ov001_021dfb94(0x38, -1, 0);
}
