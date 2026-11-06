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
extern u32 native_fn_020adfbc();
extern u32 native_fn_020b2c88();
extern u8 native_data_020e0c6c[];
u32 native_main_020ae098(s32 arg0, s32 arg1, s32 *arg2, s32 *arg3, s32 *arg4) {
    s32 sp4;
    s32 sp0;
    u8 temp_r4;
    u8 temp_r5;

    sp0 = arg0;
    temp_r4 = (u8) (arg1 >> 0x18);
    temp_r5 = (u8) (arg1 >> 0x10);
    sp4 = (s32) (u16) arg1;
    if (native_fn_020adfbc(temp_r4, temp_r5, sp4) == 0) {
        native_fn_020b2c88(sp0, native_data_020e0c6c);
        return 2U;
    }
    *arg2 = (s32) temp_r4;
    *arg3 = (s32) temp_r5;
    *arg4 = sp4;
    return 0U;
}
