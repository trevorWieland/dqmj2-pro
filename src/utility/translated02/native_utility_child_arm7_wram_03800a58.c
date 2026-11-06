typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_03806924[];
u32 native_utility_child_arm7_wram_03800a58(s32 arg0, s32 arg1) {
    u8 temp_r0;

    if (arg1 > 0xF) {
        return 0U;
    }
    temp_r0 = M2C_FIELD((arg0 + arg1), u8 *, 8);
    if (temp_r0 == 0xFF) {
        return 0U;
    }
    return (u32) (native_utility_child_arm7_data_03806924 + (temp_r0 << 6));
}
