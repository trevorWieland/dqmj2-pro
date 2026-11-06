typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_0380911c[];
extern u8 native_utility_child_arm7_data_04000000[];
u32 native_utility_child_arm7_wram_0380409c(u32 arg0) {
    if (arg0 < 0x10000U) {
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x36) = 0;
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x34) = (s16) (0x10000 - arg0);
        return 1U;
    }
    if (arg0 < 0x400000U) {
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x36) = 1;
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x34) = (s16) (0x10000 - (arg0 >> 6));
        return 1U;
    }
    if (arg0 < 0x01000000U) {
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x36) = 2;
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x34) = (s16) (0x10000 - (arg0 >> 8));
        return 1U;
    }
    if (arg0 < (u32) native_utility_child_arm7_data_04000000) {
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x36) = 3;
        M2C_FIELD(native_utility_child_arm7_data_0380911c, s16 *, 0x34) = (s16) (0x10000 - (arg0 >> 0xA));
        return 1U;
    }
    return 0U;
}
