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
extern u32 native_fn_020a40c0();
extern u32 native_fn_020bab8c();
typedef struct {
    u8 unknown_0[0x20];
    s32 field_20;
} Record_native_data_021d3044;
extern Record_native_data_021d3044 native_data_021d3044;
u32 native_main_020babac(s32 arg0) {
    native_data_021d3044.field_20 = arg0;
    if (native_fn_020a40c0(native_fn_020bab8c) != 0) {
        return 1U;
    }
    return 0U;
}
