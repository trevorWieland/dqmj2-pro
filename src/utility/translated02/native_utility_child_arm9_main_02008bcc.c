typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02008bcc(void *arg0, s32 arg1, s32 arg2) {
    if (arg2 < 0) {
        M2C_FIELD(arg0, s16 *, 0) = (s16) (arg1 | 0xC0);
        M2C_FIELD(arg0, s16 *, 4) = (s16) (0 - arg2);
        return (u32) arg0;
    }
    M2C_FIELD(arg0, s16 *, 0) = (s16) (arg1 | 0x80);
    M2C_FIELD(arg0, s16 *, 4) = (s16) arg2;
    return (u32) arg0;
}
