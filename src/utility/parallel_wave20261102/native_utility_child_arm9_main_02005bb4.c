typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02005bb4(u32 *arg0, s8 arg1) {
    u32 temp_r0;

    temp_r0 = *arg0;
    if (temp_r0 != 0) {
        CHILD_FIELD(temp_r0, s8 *, 0x40) = arg1;
    }
    return (u32) temp_r0;
}
