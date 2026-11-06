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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0208e8bc();
typedef struct {
    s32 field_0;
    s32 field_4;
} Record_native_data_021cfd58;
extern Record_native_data_021cfd58 native_data_021cfd58;
u32 native_main_0209009c(u32 arg0) {
    s32 temp_r4;
    s32 temp_r5;
    u32 temp_r6;
    u32 temp_r7;

    temp_r7 = native_fn_02007ff4();
    temp_r4 = native_data_021cfd58.field_0;
    temp_r5 = native_data_021cfd58.field_4;
    native_data_021cfd58.field_0 = 0;
    native_data_021cfd58.field_4 = 0;
    temp_r6 = native_fn_0208e8bc(arg0);
    native_data_021cfd58.field_0 = temp_r4;
    native_data_021cfd58.field_4 = temp_r5;
    native_fn_02008008(temp_r7);
    return temp_r6;
}
