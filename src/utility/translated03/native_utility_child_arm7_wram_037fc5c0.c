typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fc558(u32, u32);
extern u8 native_utility_child_arm7_data_038059d4[];
u32 native_utility_child_arm7_wram_037fc5c0(void) {
    native_utility_child_arm7_arm_037fe41c();
    return native_utility_child_arm7_arm_037fc558(M2C_FIELD(native_utility_child_arm7_data_038059d4, u32 *, 4), 0U);
}
