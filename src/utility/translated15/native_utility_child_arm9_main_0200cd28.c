typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200cd14(void);
extern u32 native_utility_child_arm9_thumb_0200a888(void);
extern u32 native_utility_child_arm9_data_0202b220[];
extern u32 native_utility_child_arm9_data_0202b224[];
u32 native_utility_child_arm9_main_0200cd28(u32 arg0, s32 arg1) {
    s32 var_r0_2;
    u32 var_r0;

    if ((arg1 & 0x3F) == 0x11) {
        var_r0 = *native_utility_child_arm9_data_0202b220;
        if (var_r0 == 0) {
            var_r0_2 = 0;
            if (*native_utility_child_arm9_data_0202b224 != 0) {
                var_r0_2 = ((s32 (*)()) *native_utility_child_arm9_data_0202b224)();
            }
            if (var_r0_2 != 0) {
                native_utility_child_arm9_thumb_0200cd14();
            }
            *native_utility_child_arm9_data_0202b220 = 1;
            return (u32) native_utility_child_arm9_data_0202b220;
        }
        
        return var_r0;
    }
    var_r0 = native_utility_child_arm9_thumb_0200a888();
    return var_r0;
}
