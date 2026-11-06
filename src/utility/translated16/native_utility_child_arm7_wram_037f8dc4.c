typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037f899c(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_037f8558(u32, u32);
extern u32 native_utility_child_arm7_arm_037fcccc(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_037f878c(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_wram_037f8dc4(u32 arg0, u32 arg1) {
    if (M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x1FC) != 0) {
        native_utility_child_arm7_arm_037f899c(arg0, *native_utility_child_arm7_data_0380fff4 + 0x1F4, arg1);
        return native_utility_child_arm7_arm_037f8558(2U, 0x13U);
    }
    if (native_utility_child_arm7_arm_037fcccc(M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u32 *, 0x304), arg1, 0U) != 0) {
        return native_utility_child_arm7_arm_037f878c(arg0, arg1);
    }
    return native_utility_child_arm7_arm_037f899c(arg0, *native_utility_child_arm7_data_0380fff4 + 0x1F4, arg1);
}
