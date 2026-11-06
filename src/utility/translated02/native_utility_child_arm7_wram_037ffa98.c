typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_038054e0[];
u32 native_utility_child_arm7_wram_037ffa98(void *arg0, s32 arg1) {
    if (arg1 < 0x6D) {
        M2C_FIELD(arg0, u8 *, 0x1C) = (u8) (0xFF - arg1);
        return (u32) arg0;
    }
    M2C_FIELD(arg0, u8 *, 0x1C) = (u8) native_utility_child_arm7_data_038054e0[0x7F - arg1];
    return (u32) arg0;
}
