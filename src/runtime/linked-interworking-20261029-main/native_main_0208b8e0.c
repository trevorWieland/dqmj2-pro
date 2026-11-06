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
extern u32 native_fn_020069f8();
extern u32 native_fn_02006b7c();
typedef struct {
    u8 unknown_0[0x24];
    s32 field_24;
} Record_native_data_021cfcf8;
extern Record_native_data_021cfcf8 native_data_021cfcf8;
u32 native_main_0208b8e0(void) {
    if (native_data_021cfcf8.field_24 == 0) {
        return native_fn_020069f8();
    }
    return native_fn_02006b7c();
}
