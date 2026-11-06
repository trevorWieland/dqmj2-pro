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
extern u32 native_fn_0202a44c();
extern u32 native_fn_0203631c();
u32 native_main_02087f38(u32 arg0, u32 arg1, u32 arg2, s32 arg3) {
    u32 temp_r0;

    temp_r0 = native_fn_0202a44c(6, 0x18, 4);
    if (temp_r0 == 0) {
        goto block_2;
    }
    native_fn_0203631c(temp_r0, arg2, arg0, arg1, arg3);
block_2:
    return temp_r0;
}
