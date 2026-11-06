typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03803c2c(void);
extern u32 native_utility_child_arm7_data_03808174[];
u32 native_utility_child_arm7_wram_037f8000(void) {
    u32 var_r0;

    var_r0 = *native_utility_child_arm7_data_03808174;
    if (var_r0 != 0) {
        var_r0 = native_utility_child_arm7_thumb_03803c2c();
    }
    return var_r0;
}
