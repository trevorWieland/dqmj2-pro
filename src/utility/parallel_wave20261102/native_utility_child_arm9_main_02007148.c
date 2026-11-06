typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02005eb4(u32);
u32 native_utility_child_arm9_main_02007148(u32 arg0) {
    s32 temp_r1;

    temp_r1 = CHILD_FIELD(arg0, s32 *, 0x120);
    if (temp_r1 == 0) {
        return (u32) arg0;
    }
    CHILD_FIELD(arg0, s32 *, 0x120) = (s32) (temp_r1 - 1);
    if (CHILD_FIELD(arg0, s32 *, 0x120) != 0) {
        return (u32) arg0;
    }
    return native_utility_child_arm9_arm_02005eb4((u32) arg0);
}
