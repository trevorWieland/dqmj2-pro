typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_0202b120[];
u32 native_utility_child_arm9_main_0200b67c(void) {
    s32 var_r2;
    u8 *var_r1;

    var_r2 = 0;
    var_r1 = native_utility_child_arm9_data_0202b120;
    do {
        M2C_FIELD(var_r1, s32 *, 0) = 0;
        M2C_FIELD(var_r1, s32 *, 4) = 0;
        M2C_FIELD(var_r1, s8 *, 8) = 0;
        var_r1 += 0xC;
        var_r2 += 1;
    } while (var_r2 < 8);
    return 0U;
}
