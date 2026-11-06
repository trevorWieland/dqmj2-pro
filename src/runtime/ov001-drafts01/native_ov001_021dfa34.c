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
extern u32 native_fn_ov001_021e66f8();
extern u32 native_fn_ov001_021fbf80();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021dfa34(void) {
    if (native_fn_ov001_021fbf80() != 0) {
        native_fn_ov001_021e66f8(3);
        native_data_ov001_022388ec.field_8 = 0x36;
    }
    return 0U;
}
