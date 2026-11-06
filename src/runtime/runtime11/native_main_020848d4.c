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
extern u32 native_fn_02008c14();
extern u8 native_data_021c96b0[];
void native_main_020848d4(s32 arg0) {
    u8 var_r7;

    var_r7 = 0;
loop_1:
    native_fn_02008c14(0, (var_r7 * 0xB0) + ((arg0 * 0x1810) + (s32) native_data_021c96b0), 0xB0);
    var_r7 += 1;
    if ((u32) var_r7 < 0x23U) {
        goto loop_1;
    }
    return;
}
