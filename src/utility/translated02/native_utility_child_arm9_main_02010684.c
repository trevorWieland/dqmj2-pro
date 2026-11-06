typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_020106a4(u32, u32);
extern u32 native_utility_child_arm9_thumb_02010a70(void);
extern u8 native_utility_child_arm9_data_02010a6d[];
u32 native_utility_child_arm9_main_02010684(void) {
    u32 sp0;
    u32 var_r0;

    var_r0 = native_utility_child_arm9_thumb_020106a4((u32) native_utility_child_arm9_data_02010a6d, (u32) &sp0);
    if (var_r0 == 0) {
        native_utility_child_arm9_thumb_02010a70();
        var_r0 = sp0;
    }
    return var_r0;
}
