typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_020076d4(s32 arg0) {
    s32 var_r2;

    var_r2 = 0;
loop_1:
    if (*(u8 *)(arg0 + var_r2) != 0) {
        return 1U;
    }
    var_r2 += 1;
    if (var_r2 >= 0x20) {
        return 0U;
    }
    goto loop_1;
}
