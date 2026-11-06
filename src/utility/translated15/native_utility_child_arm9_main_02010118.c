typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f8d4(void);
extern u32 native_utility_child_arm9_thumb_0200fa48(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200fa74(u32, u32);
extern u16 native_utility_child_arm9_data_0202cc4c[];
extern u8 native_utility_child_arm9_data_0202cc50[];
extern u8 native_utility_child_arm9_data_0201016d[];
u32 native_utility_child_arm9_main_02010118(void) {
    u16 *var_r0;

    var_r0 = native_utility_child_arm9_data_0202cc4c;
    if (*native_utility_child_arm9_data_0202cc4c == 0) {
        *native_utility_child_arm9_data_0202cc4c = 1;
        native_utility_child_arm9_thumb_0200f8d4();
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s16 *, 0xC) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s32 *, 0) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s32 *, 0x10) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s16 *, 0x32) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s16 *, 0x30) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s16 *, 0x36) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202cc50, s16 *, 0x34) = 0;
        do {

        } while (native_utility_child_arm9_thumb_0200fa48(6U, 1U) == 0);
        var_r0 = (u16 *) native_utility_child_arm9_thumb_0200fa74(6U, (u32) native_utility_child_arm9_data_0201016d);
    }
    return (u32) var_r0;
}
