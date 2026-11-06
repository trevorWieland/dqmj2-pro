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
#define NULL ((void *)0)
extern u32 native_fn_02045ed0(s32);
extern u32 native_fn_02061c1c(s32,u32,u32,u32,u32,u32,u32);
u32 native_main_02070580(void) {
    s8 var_r10;
    s8 var_r11;
    s8 var_r7;
    u8 var_r8;
    u8 var_r9;

    var_r8 = 2;
    var_r11 = 0;
    var_r10 = 6;
loop_1:
    var_r9 = 8;
    var_r7 = 0;
loop_2:
    native_fn_02061c1c(var_r10, var_r8, var_r9, 0xE, 2, 0, 0);
    var_r9 += 2;
    var_r10 += 1;
    if ((s32) var_r10 < 0x14) {
        var_r7 += 1;
        if ((s32) var_r7 < 7) {
            goto loop_2;
        }
    }
    if ((s32) var_r10 < 0x14) {
        var_r8 += 0x10;
        var_r11 += 1;
        if ((s32) var_r11 < 2) {
            goto loop_1;
        }
    }
    return native_fn_02045ed0(1);
}
