typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b44c(u32);
extern u32 native_utility_child_arm9_thumb_0200b418(u32);
u32 native_utility_child_arm9_main_0200ae98(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u32 var_r0;

    var_r0 = native_utility_child_arm9_thumb_0200b44c(1U);
    if (var_r0 != 0) {
        M2C_FIELD(var_r0, s32 *, 4) = arg0;
        M2C_FIELD(var_r0, s32 *, 8) = arg1;
        M2C_FIELD(var_r0, s32 *, 0xC) = arg2;
        M2C_FIELD(var_r0, s32 *, 0x10) = arg3;
        M2C_FIELD(var_r0, s32 *, 0x14) = arg4;
        var_r0 = native_utility_child_arm9_thumb_0200b418(var_r0);
    }
    return var_r0;
}
