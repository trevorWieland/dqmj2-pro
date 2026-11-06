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
extern u32 native_arm7_data_03808660;
u32 native_arm7_wram_03800a7c(s32 arg0, s32 arg1) {
    u8 temp_r1;

    if (arg1 > 0xF) {
        return 0U;
    }
    temp_r1 = M2C_FIELD((arg0 + arg1), u8 *, 8);
    if (temp_r1 == 0xFF) {
        return 0U;
    }
    return (u32) ((u32) &native_arm7_data_03808660 + (temp_r1 << 6));
}
