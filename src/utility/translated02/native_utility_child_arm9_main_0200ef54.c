typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200ef6c(void);
extern u32 native_utility_child_arm9_thumb_0200a888(void);
u32 native_utility_child_arm9_main_0200ef54(void) {
    u32 var_r0;

    var_r0 = native_utility_child_arm9_thumb_0200ef6c();
    if (var_r0 == 0) {
        var_r0 = native_utility_child_arm9_thumb_0200a888();
    }
    return var_r0;
}
