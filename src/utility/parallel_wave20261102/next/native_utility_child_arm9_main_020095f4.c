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
extern u32 native_utility_child_arm9_thumb_02009a2c(u32, u32);
extern u32 native_utility_child_arm9_thumb_020098c4(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
#define native_utility_child_arm9_data_020292f8 ((volatile u32 *)0x20292f8)
u32 native_utility_child_arm9_main_020095f4(u32 arg0) {
    u32 temp_r6;
    u32 temp_r4;

    temp_r6 = native_utility_child_arm9_arm_0200a64c();
    temp_r4 = *(u32 *)(*native_utility_child_arm9_data_020292f8);
    if (arg0 != 0) {
        CHILD_FIELD(temp_r4, u32 *, 0x78) = arg0;
        native_utility_child_arm9_thumb_02009a2c(arg0, (u32) temp_r4);
    }
    CHILD_FIELD(temp_r4, s32 *, 0x64) = 0;
    native_utility_child_arm9_thumb_020098c4();
    return native_utility_child_arm9_arm_0200a660(temp_r6);
}
