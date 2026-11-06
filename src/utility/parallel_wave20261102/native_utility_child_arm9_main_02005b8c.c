typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b004(u32, u32);
u32 native_utility_child_arm9_main_02005b8c(u32 *arg0, u32 arg1) {
    u32 temp_r0;

    temp_r0 = *arg0;
    if (temp_r0 == 0) {
        return (u32) temp_r0;
    }
    return native_utility_child_arm9_thumb_0200b004((u32) CHILD_FIELD(temp_r0, u8 *, 0x3C), arg1);
}
