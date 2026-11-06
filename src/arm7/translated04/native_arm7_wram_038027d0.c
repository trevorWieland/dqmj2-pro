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
extern u32 native_arm7_fn_03802860(u32, u32, u32, u32);
extern u32 native_arm7_data_038096c0;
extern u32 native_arm7_data_0380727c;
extern u32 native_arm7_data_03802924;
extern u32 native_arm7_data_038028e4;
u32 native_arm7_wram_038027d0(void) {
    u8 sp0;

    M2C_FIELD(&native_arm7_data_038096c0, s32 *, 4) = 2;
    native_arm7_fn_03802860((u32) &native_arm7_data_0380727c, 0U, 1U, (u32) &native_arm7_data_03802924);
    native_arm7_fn_03802860(0U, (u32) &sp0, 1U, (u32) &native_arm7_data_038028e4);
    return (u32) sp0;
}
