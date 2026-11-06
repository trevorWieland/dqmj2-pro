typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200c714(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200c750(u32, u32, u32);
extern u32 native_utility_child_arm9_data_02028710[];
u32 native_utility_child_arm9_main_020061a4(u32 arg0, u32 arg1, u32 arg2, s32 arg3) {
    u32 var_r5;
    u32 temp_r4;
    void *temp_r2;
    void *temp_r1;
    u32 temp_r0;

    var_r5 = arg2;
    temp_r4 = *native_utility_child_arm9_data_02028710;
    temp_r2 = M2C_FIELD(temp_r4, void **, 0x84);
    if (arg0 >= (u32) M2C_FIELD(temp_r2, u32 *, 8)) {
        return -1U;
    }
    temp_r1 = temp_r2 + 0xC + (arg0 * 0x10);
    temp_r0 = M2C_FIELD(temp_r1, s32 *, 4) - arg3;
    if (var_r5 > temp_r0) {
        var_r5 = temp_r0;
    }
    if (native_utility_child_arm9_thumb_0200c714(temp_r4 + 0x34, M2C_FIELD(temp_r1, s32 *, 0) + arg3, 0U) == 0) {
        return -1U;
    }
    return native_utility_child_arm9_thumb_0200c750(temp_r4 + 0x34, arg1, var_r5);
}
