typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02002ab0(u32);
extern u32 native_utility_child_arm9_thumb_0200ee4c(u32, u32);
extern u32 native_utility_child_arm9_thumb_02002abc(u32);
extern u8 native_utility_child_arm9_data_02027ce8[];
u32 native_utility_child_arm9_main_02002db4(void) {
    s32 temp_r0;
    u32 temp_r0_2;

    temp_r0 = M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027ce8, void **, 4), s32 *, 0x40);
    if (temp_r0 == 6) {
        return 1U;
    }
    if (temp_r0 != 4) {
        return 0U;
    }
    native_utility_child_arm9_thumb_02002ab0(6U);
    temp_r0_2 = native_utility_child_arm9_thumb_0200ee4c((u32) (M2C_FIELD(native_utility_child_arm9_data_02027ce8, void **, 4) + 0x1E00), 0xDU);
    if (temp_r0_2 != 2) {
        native_utility_child_arm9_thumb_02002abc(temp_r0_2);
        return 0U;
    }
    return 1U;
}
