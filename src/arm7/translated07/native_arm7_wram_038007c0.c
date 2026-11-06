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
extern u32 native_arm7_fn_03800290(u32);
u32 native_arm7_wram_038007c0(u32 arg0) {
    s32 temp_r4;
    u32 temp_r4_2;

    temp_r4_2 = native_arm7_fn_03800290(arg0);
    temp_r4 = temp_r4_2 | (native_arm7_fn_03800290(arg0) << 8);
    return temp_r4 | (native_arm7_fn_03800290(arg0) << 0x10);
}
