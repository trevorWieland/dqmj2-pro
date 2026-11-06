typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_038021c0(void);
extern u32 native_utility_child_arm7_thumb_03802098(void);
extern u32 native_utility_child_arm7_thumb_0380229c(u32);
extern u32 native_utility_child_arm7_thumb_03802160(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_03802238(u32, u32);
extern u32 native_utility_child_arm7_data_03807380[];
extern u8 native_utility_child_arm7_data_038054f4[];
extern u8 native_utility_child_arm7_data_03802105[];
u32 native_utility_child_arm7_wram_03801d5c(void) {
    u32 var_r0;
    u32 temp_r4;

    var_r0 = native_utility_child_arm7_thumb_038021c0();
    if (var_r0 != 0) {
        temp_r4 = *native_utility_child_arm7_data_03807380;
        native_utility_child_arm7_thumb_03802098();
        native_utility_child_arm7_thumb_0380229c(1U);
        native_utility_child_arm7_thumb_03802160((u32) native_utility_child_arm7_data_038054f4, 0U, 1U, (u32) native_utility_child_arm7_data_03802105);
        var_r0 = native_utility_child_arm7_thumb_03802238(M2C_FIELD(temp_r4, u32 *, 0x34), M2C_FIELD(temp_r4, u32 *, 0x38));
    }
    return var_r0;
}
