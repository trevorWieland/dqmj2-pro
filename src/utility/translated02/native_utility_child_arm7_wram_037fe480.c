typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_03804f78(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_arm_037fc0ac(void);
u32 native_utility_child_arm7_wram_037fe480(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    native_utility_child_arm7_arm_03804f78(arg0, 4U, arg2, arg3);
    return native_utility_child_arm7_arm_037fc0ac();
}
