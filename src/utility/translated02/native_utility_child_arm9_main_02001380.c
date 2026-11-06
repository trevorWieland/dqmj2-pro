typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02026600[];
u32 native_utility_child_arm9_main_02001380(u8 *arg0) {
    u8 *var_r0;

    var_r0 = arg0;
    if (var_r0 == (u8 *)1) {
        M2C_FIELD(native_utility_child_arm9_data_02026600, s8 *, 1) = 1;
        M2C_FIELD(native_utility_child_arm9_data_02026600, s32 *, 8) = 0;
        return (u32) native_utility_child_arm9_data_02026600;
    }
    if (var_r0 == (u8 *)2) {
        var_r0 = native_utility_child_arm9_data_02026600;
        M2C_FIELD(native_utility_child_arm9_data_02026600, s8 *, 1) = 2;
        M2C_FIELD(native_utility_child_arm9_data_02026600, s32 *, 8) = 1;
    }
    return (u32) var_r0;
}
