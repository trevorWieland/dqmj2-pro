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
u32 native_arm7_main_027ebe98(s32 arg0) {
    s32 temp_r1;
    u16 temp_r0;

    temp_r1 = (arg0 * 0x1C) + M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x31C);
    temp_r0 = M2C_FIELD(temp_r1, u16 *, 0x1A);
    M2C_FIELD(temp_r1, u16 *, 0x18) = temp_r0;
    return (u32) temp_r0;
}
