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
extern u32 native_utility_child_arm7_data_03805c44;
u32 native_utility_child_arm7_wram_037fede8(u32 arg0, s32 arg1) {
    if (arg1 < 0x18) {
        return (u32) ((s32) (arg0 * ((native_utility_child_arm7_data_03805c44 * (arg1 + 0x28)) + ((0x7FFF - native_utility_child_arm7_data_03805c44) << 6))) >> 0x15);
    }
    if (arg1 <= 0x68) {
        return arg0;
    }
    return (u32) ((s32) (arg0 * (((0 - native_utility_child_arm7_data_03805c44) * (arg1 - 0x28)) + ((native_utility_child_arm7_data_03805c44 + 0x7FFF) << 6))) >> 0x15);
}
