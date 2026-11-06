typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f808(void);
extern u32 native_utility_child_arm9_thumb_0200a888(void);
extern u32 native_utility_child_arm9_data_0202cbc0[];
extern u32 native_utility_child_arm9_data_0202cbc4[];
u32 native_utility_child_arm9_main_0200f86c(u32 arg0, s32 arg1) {
    u32 var_r0;

    if ((arg1 & 0x3F) == 0x11) {
        var_r0 = *native_utility_child_arm9_data_0202cbc0;
        if (var_r0 == 0) {
            var_r0 = 1;
            *native_utility_child_arm9_data_0202cbc0 = 1;
            if (*native_utility_child_arm9_data_0202cbc4 != 0) {
                var_r0 = ((u32 (*)()) *native_utility_child_arm9_data_0202cbc4)();
            }
            if (var_r0 != 0) {
                return native_utility_child_arm9_thumb_0200f808();
            }
            
            return var_r0;
        }
        
        return var_r0;
    }
    var_r0 = native_utility_child_arm9_thumb_0200a888();
    return var_r0;
}
