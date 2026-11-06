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
extern u32 native_fn_020642dc(void);
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
} Record_native_data_021d6384;
extern Record_native_data_021d6384 native_data_021d6384;
u32 native_main_020c617c(void) {
    if ((native_fn_020642dc() != 0x1C) || (native_data_021d6384.field_1 != 1)) {
        return 1U;
    }
    return 0U;
}
