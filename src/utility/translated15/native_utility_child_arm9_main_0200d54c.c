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
extern u16 native_utility_child_arm9_data_0202b810[];
extern u8 native_utility_child_arm9_data_0202b814[];
extern u8 native_utility_child_arm9_data_0200d109[];
u32 native_utility_child_arm9_main_0200d54c(void) {
    u16 *var_r0;

    var_r0 = native_utility_child_arm9_data_0202b810;
    if (*native_utility_child_arm9_data_0202b810 == 0) {
        *native_utility_child_arm9_data_0202b810 = 1;
        M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 4) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0x1C) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 8) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202b814, s32 *, 0xC) = 0;
        native_utility_child_arm9_thumb_0200f8d4();
        do {

        } while (native_utility_child_arm9_thumb_0200fa48(5U, 1U) == 0);
        var_r0 = (u16 *) native_utility_child_arm9_thumb_0200fa74(5U, (u32) native_utility_child_arm9_data_0200d109);
    }
    return (u32) var_r0;
}
