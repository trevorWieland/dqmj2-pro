typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f1144(void);
extern u32 native_utility_child_arm7_arm_027ecc6c(void);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_wram_037faa14(void) {
    u32 var_r0;

    if (M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x3E8) != 0) {
        native_utility_child_arm7_arm_027f1144();
    }
    var_r0 = (u32) (M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x33A) << 0x19) >> 0x1F;
    if (var_r0 != 0) {
        var_r0 = native_utility_child_arm7_arm_027ecc6c();
    }
    return var_r0;
}
