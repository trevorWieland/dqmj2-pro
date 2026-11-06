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
extern u32 native_fn_0208d764();
extern u32 native_fn_0208d780();
extern u32 native_fn_0208d7c0();
extern u32 native_fn_0208d7e0();
extern u32 native_fn_0208e1e4();
extern u32 native_fn_0208e2e0();
u32 native_main_0208e4fc(void) {
    u32 temp_r0;
    s32 var_r5;

    native_fn_0208d7c0();
    native_fn_0208d764();
    native_fn_0208d780(0x44, 0x43, -1);
    var_r5 = 0;
loop_1:
    temp_r0 = native_fn_0208e2e0(native_fn_0208e1e4(), var_r5);
    if (temp_r0 != 1) {
        var_r5 += 1;
        if (var_r5 < 4) {
            goto loop_1;
        }
    }
    native_fn_0208d7e0();
    if (temp_r0 == 1) {
        return 1U;
    }
    return 0U;
}
