typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02027b7c[];
u32 native_utility_child_arm9_main_02001efc(void) {
    s32 var_r1;
    u8 *var_r2;

    var_r1 = 0;
    var_r2 = native_utility_child_arm9_data_02027b7c;
    do {
        M2C_FIELD(var_r2, s8 *, 0x18) = 0;
        M2C_FIELD(var_r2, s32 *, 0x10) = 0;
        M2C_FIELD(var_r2, s32 *, 0x14) = 0;
        var_r1 += 1;
        var_r2 += 0x1C;
    } while (var_r1 < 0xA);
    return 0U;
}
