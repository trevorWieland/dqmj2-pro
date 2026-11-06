typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200ac54(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02002f14(void);
extern u32 native_utility_child_arm9_thumb_02003088(u32);
extern u32 native_utility_child_arm9_thumb_02003068(u32);
extern u8 native_utility_child_arm9_data_02027cd8[];
void native_utility_child_arm9_main_02002848(s16 arg0, s16 arg1, u32 arg2) {
    u32 temp_r0;
    u32 var_r5;

    *M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s16 **, 0xA40) = arg0;
    M2C_FIELD(M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s16 **, 0xA40), s16 *, 2) = arg1;
    native_utility_child_arm9_arm_0200ac54(arg2, (u32) (M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s16 **, 0xA40) + 2), 0x40U);
    if (native_utility_child_arm9_thumb_02002f14() == 5) {
        if (native_utility_child_arm9_thumb_02003088((u32) (M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4) + 0x800)) == 0) {
            M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s32 *, 0x1254) = (s32) (M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s32 *, 0x1254) + 1);
        } else {
            M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s32 *, 0x1254) = 0;
        }
        var_r5 = 0;
        do {
            temp_r0 = native_utility_child_arm9_thumb_02003068(var_r5);
            if (temp_r0 != 0) {
                native_utility_child_arm9_arm_0200ac54(temp_r0, (u32) (M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4) + 0x900 + (var_r5 * 0x44)), 0x44U);
                M2C_FIELD((M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4) + (var_r5 * 4)), s32 *, 0xA00) = 1;
            } else {
                M2C_FIELD((M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4) + (var_r5 * 4)), s32 *, 0xA00) = 0;
            }
            var_r5 = (u32) (u16) (var_r5 + 1);
        } while (var_r5 < 2U);
        return;
    }
    M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s32 *, 0x1254) = (s32) (M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s32 *, 0x1254) + 1);
}
