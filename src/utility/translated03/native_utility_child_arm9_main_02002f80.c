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
extern u32 native_utility_child_arm9_thumb_0200e238(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02002abc(u32);
extern u8 native_utility_child_arm9_data_02027ce8[];
extern u8 native_utility_child_arm9_data_02002fb5[];
u32 native_utility_child_arm9_main_02002f80(void) {
    u32 temp_r0;

    native_utility_child_arm9_thumb_02002ab0(3U);
    temp_r0 = native_utility_child_arm9_thumb_0200e238(M2C_FIELD(native_utility_child_arm9_data_02027ce8, s32 *, 4) + 0x80, (u32) native_utility_child_arm9_data_02002fb5, 2U);
    if (temp_r0 != 2) {
        native_utility_child_arm9_thumb_02002abc(temp_r0);
        native_utility_child_arm9_thumb_02002ab0(0xAU);
        return 0U;
    }
    return 1U;
}
