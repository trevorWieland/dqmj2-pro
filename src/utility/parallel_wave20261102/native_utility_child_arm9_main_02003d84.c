typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02003d84(u32 arg0, u32 arg1) {
    CHILD_FIELD(arg0, s32 *, 0) = (s32) (arg1 - (u16) (((s32) CHILD_FIELD(arg1, u16 *, 2) >> 8) & 0x7F));
    CHILD_FIELD(arg0, u32 *, 4) = (u32 ) (CHILD_FIELD(arg1, s32 *, 4) + (arg1 + 0x10));
    return (u32) arg0;
}
