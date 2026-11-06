typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_02003720(u32, u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
#define native_utility_child_arm9_data_02028754 ((volatile u8 *)0x2028754)
u32 native_utility_child_arm9_main_020070a4(u32 arg0) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_arm_0200a64c();
    native_utility_child_arm9_arm_02003720((u32) native_utility_child_arm9_data_02028754, arg0);
    return native_utility_child_arm9_arm_0200a660(temp_r4);
}
