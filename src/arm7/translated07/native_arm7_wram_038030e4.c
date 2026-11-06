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
extern u32 native_arm7_fn_03803114(u32, u32, u32);
extern u32 native_arm7_fn_03803094(void);
extern u32 native_arm7_fn_03802ffc(void);
extern u32 native_arm7_data_038090c0;
u32 native_arm7_wram_038030e4(void) {
    u32 temp_r4;

    native_arm7_fn_03803114((u32) &native_arm7_data_038090c0, 0U, 0U);
    temp_r4 = native_arm7_fn_03803094();
    native_arm7_fn_03802ffc();
    return temp_r4;
}
