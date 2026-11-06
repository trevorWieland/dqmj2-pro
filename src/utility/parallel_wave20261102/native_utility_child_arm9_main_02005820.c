typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b044(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200afe4(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_02005734(u32);
extern u32 native_utility_child_arm9_thumb_0200b270(void);
u32 native_utility_child_arm9_main_02005820(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r2;
    u32 temp_r4;

    temp_r4 = CHILD_FIELD(arg0, u32 *, 4);
    native_utility_child_arm9_thumb_0200b044((u32) CHILD_FIELD(arg0, u8 *, 0x3C), arg1, arg2, arg3);
    temp_r2 = CHILD_FIELD(temp_r4, u32 *, 0x1C);
    if (temp_r2 != 0) {
        native_utility_child_arm9_thumb_0200afe4((u32) CHILD_FIELD(arg0, u8 *, 0x3C), 0xFFFFU, temp_r2);
    }
    native_utility_child_arm9_arm_02005734((u32) arg0);
    CHILD_FIELD(arg0, u32 *, 0x30) = native_utility_child_arm9_thumb_0200b270();
    CHILD_FIELD(arg0, s8 *, 0x2F) = 1;
    CHILD_FIELD(arg0, s8 *, 0x2C) = 1;
    return 1U;
}
