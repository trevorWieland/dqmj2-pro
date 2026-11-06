typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_038023b8(u32);
extern u8 native_utility_child_arm7_data_03807bf0[];
extern u8 native_utility_child_arm7_data_03808080[];
u32 native_utility_child_arm7_wram_03802ac0(u32 arg0) {
    u32 var_r0;

    var_r0 = arg0;
    if (M2C_FIELD(native_utility_child_arm7_data_03807bf0, s32 *, 4) == var_r0) {
        M2C_FIELD(native_utility_child_arm7_data_03807bf0, s32 *, 4) = 5;
        M2C_FIELD(native_utility_child_arm7_data_03807bf0, s32 *, 0) = 0;
        var_r0 = native_utility_child_arm7_thumb_038023b8((u32) native_utility_child_arm7_data_03808080);
    }
    return var_r0;
}
