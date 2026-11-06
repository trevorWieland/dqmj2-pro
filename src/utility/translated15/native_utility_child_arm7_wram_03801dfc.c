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
extern u8 native_utility_child_arm7_data_038079a4[];
extern u8 native_utility_child_arm7_data_038020c5[];
u32 native_utility_child_arm7_wram_03801dfc(u32 arg0, u32 arg1, u32 arg2) {
    u32 var_r0;
    u32 temp_r4;

    var_r0 = native_utility_child_arm7_thumb_038021c0();
    if (var_r0 != 0) {
        temp_r4 = *native_utility_child_arm7_data_03807380;
        M2C_FIELD(native_utility_child_arm7_data_038079a4, u32 *, 0xC) = 1U;
        native_utility_child_arm7_thumb_0380229c(M2C_FIELD(temp_r4, s32 *, 0x24) + 1 + arg2);
        native_utility_child_arm7_thumb_03802018(arg0, 3U);
        native_utility_child_arm7_thumb_03802160(arg1, 0U, arg2, (u32) native_utility_child_arm7_data_038020c5);
        native_utility_child_arm7_thumb_03802238(0U, 0U);
        var_r0 = M2C_FIELD(temp_r4, u32 *, 0);
        if (var_r0 == 0) {
            var_r0 = M2C_FIELD(native_utility_child_arm7_data_038079a4, u32 *, 0xC);
            if (var_r0 == 0) {
                var_r0 = 1;
                M2C_FIELD(temp_r4, u32 *, 0) = 1U;
            }
        }
    }
    return var_r0;
}
