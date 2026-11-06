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
extern u32 native_fn_020068d4();
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0208f900();
u32 native_main_0208f898(void *arg0, s32 arg1, s32 arg2, s32 *arg3, s32 arg4) {
    u32 temp_r0;
    void *temp_r4;
    s32 var_r5;
    u32 spC;
    u32 sp8;
    s32 *sp4;
    s32 sp0;

    var_r5 = arg2;
    sp0 = arg1;
    sp4 = arg3;
    temp_r4 = M2C_FIELD(arg0, void **, 0x68);
    if (var_r5 > arg1) {
        var_r5 = arg1;
    }
    sp8 = native_fn_02007ff4();
loop_3:
    temp_r0 = native_fn_0208f900(arg0);
    spC = temp_r0;
    if ((s32) temp_r0 >= var_r5) {
        if ((s32) temp_r0 >= sp0) {
            spC = sp0;
        }
        *sp4 = (s32) M2C_FIELD(temp_r4, u16 *, 0x100);
    } else if (!(arg4 & 1)) {
        spC = 0;
    } else {
        native_fn_020068d4(temp_r4 + 0x104);
        goto loop_3;
    }
    native_fn_02008008(sp8);
    return spC;
}
