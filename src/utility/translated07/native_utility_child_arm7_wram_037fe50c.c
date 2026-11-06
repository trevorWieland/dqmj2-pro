typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe53c(u32, u32, u32);
u32 native_utility_child_arm7_wram_037fe50c(s32 arg0) {
    u32 temp_r0;

    do {
        temp_r0 = native_utility_child_arm7_arm_037fe53c(0xCU, arg0 << 8, 0U);
    } while (temp_r0 != 0);
    return temp_r0;
}
