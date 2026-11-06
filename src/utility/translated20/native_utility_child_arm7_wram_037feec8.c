typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_04000403 ((volatile u8 *)0x4000403)
u32 native_utility_child_arm7_wram_037feec8(s32 arg0) {
    if (*((arg0 * 0x10) + native_utility_child_arm7_data_04000403) & 0x80) {
        return 1U;
    }
    return 0U;
}
