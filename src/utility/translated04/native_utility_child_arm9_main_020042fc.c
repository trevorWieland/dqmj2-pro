typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02005118(u32, u32);
extern u8 native_utility_child_arm9_data_020052d8[];
u32 native_utility_child_arm9_main_020042fc(u32 arg0, u32 arg1) {
    s16 var_r1;

    M2C_FIELD(arg0, u16 *, 8) = (u16) (native_utility_child_arm9_arm_02005118(arg1, arg0) - 1);
    if (M2C_FIELD(arg0, u16 *, 8) != 0) {
        var_r1 = 2;
    } else {
        var_r1 = 3;
    }
    M2C_FIELD(arg0, s16 *, 0xA) = var_r1;
    M2C_FIELD(arg0, u8 **, 4) = native_utility_child_arm9_data_020052d8;
    return (u32) native_utility_child_arm9_data_020052d8;
}
