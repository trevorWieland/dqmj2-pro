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
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
} Record_native_data_ov000_022463a0;
extern Record_native_data_ov000_022463a0 native_data_ov000_022463a0;
u32 native_ov000_0221f3c0(s32 arg0) {
    if (arg0 >= 0x32) {
        return 0U;
    }
    if (M2C_FIELD((native_data_ov000_022463a0.field_c + (arg0 * 7)), u8 *, 2) == 1) {
        return 1U;
    }
    return 0U;
}
