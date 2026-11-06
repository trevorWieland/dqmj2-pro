typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02003cfc(u32 arg0, s16 arg1) {
    u32 temp_r3;

    temp_r3 = CHILD_FIELD(arg0, u32 *, 0);
    CHILD_FIELD(temp_r3, s16 *, 0) = arg1;
    CHILD_FIELD(temp_r3, s16 *, 2) = 0;
    CHILD_FIELD(temp_r3, s32 *, 4) = (s32) (CHILD_FIELD(arg0, s32 *, 4) - (temp_r3 + 0x10));
    CHILD_FIELD(temp_r3, s32 *, 8) = 0;
    CHILD_FIELD(temp_r3, s32 *, 0xC) = 0;
    return (u32) temp_r3;
}
