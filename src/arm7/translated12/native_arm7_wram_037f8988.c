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
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_fn_037f87ac(u32, u32);
extern u32 native_arm7_fn_037f89f4(u32, u32);
extern u32 native_arm7_fn_037fb8f0(u32);
u32 native_arm7_wram_037f8988(u32 arg0, u32 arg1, void *arg2) {
    u32 var_r4;
    u32 temp_r5;

    if (M2C_FIELD(arg2, u16 *, 0xA) != 0xBF1D) {
        return 1U;
    }
    temp_r5 = native_arm7_fn_037fb928(0x01000000U);
    var_r4 = native_arm7_fn_037f87ac(arg0, (u32) arg2);
    if (var_r4 == 0) {
        var_r4 = native_arm7_fn_037f89f4(arg1, (u32) arg2);
    }
    native_arm7_fn_037fb8f0(temp_r5);
    return var_r4;
}
