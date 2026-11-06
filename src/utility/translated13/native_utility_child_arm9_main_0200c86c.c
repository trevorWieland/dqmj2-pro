typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200c88c(u32);
extern u32 native_utility_child_arm9_data_0202b194[];
u32 native_utility_child_arm9_main_0200c86c(u32 arg0) {
    u32 var_r0;

    var_r0 = arg0;
    if (*native_utility_child_arm9_data_0202b194 == 0) {
        *native_utility_child_arm9_data_0202b194 = 1;
        var_r0 = native_utility_child_arm9_thumb_0200c88c(var_r0);
    }
    return var_r0;
}
