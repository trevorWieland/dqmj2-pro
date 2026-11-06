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
extern u32 native_utility_child_arm7_thumb_0380229c(u32);
extern u32 native_utility_child_arm7_thumb_03802018(u32, u32);
extern u32 native_utility_child_arm7_thumb_03802160(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_03802238(u32, u32);
extern u32 native_utility_child_arm7_data_03807380[];
extern u8 native_utility_child_arm7_data_03802135[];
u32 native_utility_child_arm7_wram_03801f5c(u32 arg0, u32 arg1, u32 arg2) {
    u32 var_r0;

    var_r0 = native_utility_child_arm7_thumb_038021c0();
    if (var_r0 != 0) {
        native_utility_child_arm7_thumb_0380229c(M2C_FIELD(*native_utility_child_arm7_data_03807380, s32 *, 0x24) + 1 + arg2);
        native_utility_child_arm7_thumb_03802018(arg0, 3U);
        native_utility_child_arm7_thumb_03802160(0U, arg1, arg2, (u32) native_utility_child_arm7_data_03802135);
        var_r0 = native_utility_child_arm7_thumb_03802238(0U, 0U);
    }
    return var_r0;
}
