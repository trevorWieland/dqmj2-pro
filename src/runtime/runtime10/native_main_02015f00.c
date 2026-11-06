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
extern u32 native_fn_02008e0c();
extern u32 native_fn_02015f74();
extern u8 native_data_020d8ce0[];
u32 native_main_02015f00(void *arg0, void *arg1) {
    u8 *var_r7;
    void *var_r8;
    s32 var_r9;
    s32 sp0;

    sp0 = 0x022C0000;
    var_r7 = native_data_020d8ce0;
    M2C_FIELD(arg0, s32 *, 0) = (s32) M2C_FIELD(arg1, s32 *, 0x24);
    var_r8 = arg0 + 0xC;
    M2C_FIELD(arg0, s32 *, 4) = (s32) M2C_FIELD(arg1, s32 *, 0x34);
    var_r9 = 0;
    do {
        native_fn_02015f74(arg1, var_r7, var_r8, &sp0);
        var_r9 += 1;
        var_r8 += 0x10;
        var_r7 += 4;
    } while (var_r9 < 3);
    return native_fn_02008e0c(arg1 + 0x160, arg0 + 0x3C, 0x88);
}
