typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02003d2c(u32 arg0, u32 arg1, u32 arg2) {
    u32 var_r3;

    CHILD_FIELD(arg1, u32 *, 8) = arg2;
    if (arg2 != 0) {
        var_r3 = CHILD_FIELD(arg2, u32 *, 0xC);
        CHILD_FIELD(arg2, u32 *, 0xC) = arg1;
    } else {
        var_r3 = CHILD_FIELD(arg0, u32 *, 0);
        CHILD_FIELD(arg0, u32 *, 0) = arg1;
    }
    CHILD_FIELD(arg1, u32 *, 0xC) = var_r3;
    if (var_r3 != 0) {
        CHILD_FIELD(var_r3, u32 *, 8) = arg1;
    } else {
        CHILD_FIELD(arg0, u32 *, 4) = arg1;
    }
    return (u32) arg1;
}
