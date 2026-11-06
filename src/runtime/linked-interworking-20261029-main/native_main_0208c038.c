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
extern u32 native_fn_02006b7c();
extern u32 native_fn_0208bf10();
extern u32 native_fn_0208bf98();
typedef struct {
    u8 unknown_0[0x50];
    s32 field_50;
} Record_native_data_021cfcf8;
extern Record_native_data_021cfcf8 native_data_021cfcf8;
u32 native_main_0208c038(u32 arg0) {
    u32 temp_r0;
    u32 var_r0;
    u32 var_r4;
    u32 sp0;

    sp0 = 0;
loop_1:
    native_fn_0208bf98(arg0);
    var_r4 = 0;
loop_2:
    if (native_data_021cfcf8.field_50 == 0) {
        return 0U;
    }
    native_fn_02006b7c(0x64);
    var_r0 = native_fn_0208bf10(arg0);
    if (var_r0 == 0) {
        var_r4 += 1;
        if (var_r4 >= 0x14U) {
            temp_r0 = sp0 + 1;
            sp0 = temp_r0;
            if (temp_r0 >= 8U) {
                var_r0 = 0;
                
                return var_r0;
            }
            goto loop_1;
        }
        goto loop_2;
    }
    return var_r0;
}
