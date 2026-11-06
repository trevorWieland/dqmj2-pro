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
extern u32 native_fn_02006e24();
extern u32 native_fn_020072ec();
extern u32 native_fn_02008e0c();
extern u32 native_fn_0200a440();
extern u32 native_fn_0201184c();
extern u8 native_data_020e5d88[];
u32 native_main_02011950(u32 arg0, u32 arg1) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r0 = native_fn_0201184c();
    if (temp_r0 == 0) {
        return 8U;
    }
    native_fn_02008e0c(arg0, temp_r0, arg1);
    native_fn_020072ec(temp_r0, arg1);
    temp_r4 = native_fn_0200a440(0xA, temp_r0, 0);
    native_fn_02006e24(native_data_020e5d88, temp_r0, 1);
    if ((s32) temp_r4 < 0) {
        return 8U;
    }
    return 2U;
}
