typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200a9ec(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_arm_0200ab2c(u32, u32, u32);
extern u32 native_utility_child_arm9_data_020225c4[];
#define native_utility_child_arm9_data_05000000 ((volatile u8 *)0x5000000)
u32 native_utility_child_arm9_main_02008e9c(u32 arg0, s32 arg1, u32 arg2) {
    if ((*native_utility_child_arm9_data_020225c4 != -1U) && (arg2 > 0x1CU)) {
        return native_utility_child_arm9_thumb_0200a9ec(*native_utility_child_arm9_data_020225c4, arg0, (u32) &native_utility_child_arm9_data_05000000[arg1], arg2);
    }
    return native_utility_child_arm9_arm_0200ab2c(arg0, (u32) &native_utility_child_arm9_data_05000000[arg1], arg2);
}
