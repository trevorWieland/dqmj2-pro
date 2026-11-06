typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02003fdc(u32 arg0) {
    CHILD_FIELD(arg0, u32 *, 0x14) = (u32 ) (CHILD_FIELD(arg0, u32 *, 0x14) + arg0);
    return (u32) arg0;
}
