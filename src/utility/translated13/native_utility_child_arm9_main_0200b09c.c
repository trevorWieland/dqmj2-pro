typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02009e30(u32);
extern u32 native_utility_child_arm9_thumb_0200b584(void);
extern u32 native_utility_child_arm9_thumb_0200b67c(void);
extern u32 native_utility_child_arm9_data_02029634[];
extern u8 native_utility_child_arm9_data_02029638[];
u32 native_utility_child_arm9_main_0200b09c(void) {
    u32 *var_r0;

    var_r0 = native_utility_child_arm9_data_02029634;
    if (*native_utility_child_arm9_data_02029634 == 0) {
        *native_utility_child_arm9_data_02029634 = 1;
        native_utility_child_arm9_thumb_02009e30((u32) native_utility_child_arm9_data_02029638);
        native_utility_child_arm9_thumb_0200b584();
        var_r0 = (u32 *) native_utility_child_arm9_thumb_0200b67c();
    }
    return (u32) var_r0;
}
