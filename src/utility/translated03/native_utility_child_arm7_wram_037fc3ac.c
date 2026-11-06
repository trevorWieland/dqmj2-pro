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
extern u32 native_utility_child_arm7_arm_037fc804(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
u32 native_utility_child_arm7_wram_037fc3ac(void *arg0) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm7_arm_037fe41c();
    M2C_FIELD(arg0, s32 *, 0x48) = 1;
    native_utility_child_arm7_arm_037fc804();
    return native_utility_child_arm7_arm_037fe430(temp_r4);
}
