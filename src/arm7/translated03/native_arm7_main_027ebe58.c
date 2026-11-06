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
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027ebe58(u32 arg0, s16 arg1) {
    M2C_FIELD(((arg0 * 0x1C) + M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x31C)), s16 *, 0x14) = arg1;
    return arg0;
}
