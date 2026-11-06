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
extern u32 native_arm7_data_03807edc;
u32 native_arm7_wram_03801c50(s32 arg0, s32 arg1, s16 arg2) {
    void *temp_r0;

    temp_r0 = (arg0 * 0x24) + native_arm7_data_03807edc + (arg1 * 2);
    M2C_FIELD(temp_r0, s16 *, 0x20) = arg2;
    return (u32) temp_r0;
}
