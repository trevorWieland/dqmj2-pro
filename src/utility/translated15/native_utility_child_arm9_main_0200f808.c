typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02010684(void);
extern u32 native_utility_child_arm9_arm_0200a6bc(u32);
extern u32 native_utility_child_arm9_thumb_0200f788(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200a888(void);
extern u16 native_utility_child_arm9_data_027fffa8[];
u32 native_utility_child_arm9_main_0200f808(void) {
    u32 var_r0;
    s32 var_r4;

    var_r4 = 1;
    if (((s32) (*native_utility_child_arm9_data_027fffa8 & 0x8000) >> 0xF) != 0) {
        var_r0 = native_utility_child_arm9_thumb_02010684();
        if (var_r0 == 4) {
            do {
                native_utility_child_arm9_arm_0200a6bc(0xA3A47U);
                var_r0 = native_utility_child_arm9_thumb_02010684();
            } while (var_r0 == 4);
        }
        if (var_r0 == 0) {
            var_r4 = 0;
        }
    }
    if (var_r4 != 0) {
        native_utility_child_arm9_thumb_0200f788(1U, 1U);
    }
    return native_utility_child_arm9_thumb_0200a888();
}
