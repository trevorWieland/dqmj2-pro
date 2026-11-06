typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_thumb_0200db0c(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
extern u32 native_utility_child_arm9_thumb_0200db20(void);
u32 native_utility_child_arm9_main_0200e054(s32 arg0) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_arm_0200a64c();
    temp_r0 = native_utility_child_arm9_thumb_0200db0c();
    if (temp_r0 != 0) {
        native_utility_child_arm9_arm_0200a660(temp_r4);
        return temp_r0;
    }
    M2C_FIELD((void *) native_utility_child_arm9_thumb_0200db20(), s32 *, 0xC8) = arg0;
    native_utility_child_arm9_arm_0200a660(temp_r4);
    return 0U;
}
