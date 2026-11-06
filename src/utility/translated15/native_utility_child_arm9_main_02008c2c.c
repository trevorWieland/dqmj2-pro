typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02008970(void);
extern u32 native_utility_child_arm9_thumb_0200aa48(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_arm_0200ab5c(u32, u32, u32);
extern u32 native_utility_child_arm9_data_020225c4[];
u32 native_utility_child_arm9_main_02008c2c(u32 arg0, s32 arg1, u32 arg2) {
    u32 temp_r2;

    temp_r2 = native_utility_child_arm9_thumb_02008970();
    if ((*native_utility_child_arm9_data_020225c4 != -1U) && (arg2 > 0x30U)) {
        return native_utility_child_arm9_thumb_0200aa48(*native_utility_child_arm9_data_020225c4, arg0, temp_r2 + arg1, arg2);
    }
    return native_utility_child_arm9_arm_0200ab5c(arg0, temp_r2 + arg1, arg2);
}
