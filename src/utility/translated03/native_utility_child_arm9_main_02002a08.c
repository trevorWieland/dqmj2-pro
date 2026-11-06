typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02027cd8[];
u32 native_utility_child_arm9_main_02002a08(void) {
    s32 var_r5;
    void *var_r6;

    var_r6 = M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4);
    var_r5 = 0;
loop_1:
    if (M2C_FIELD(var_r6, u8 *, 0xA54) != M2C_FIELD(var_r6, u8 *, 0xE54)) {
        return 0U;
    }
    var_r5 += 1;
    var_r6 += 1;
    if (var_r5 >= 0x400) {
        return 1U;
    }
    goto loop_1;
}
