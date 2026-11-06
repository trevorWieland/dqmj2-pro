typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02010b5c(u32, u32);
extern u32 native_utility_child_arm9_thumb_02010b00(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02007ac0(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02007b08(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02007b38(void);
extern u8 native_utility_child_arm9_data_0202920c[];
u32 native_utility_child_arm9_main_02007618(u32 arg0, u32 arg1) {
    s32 sp0;
    s32 temp_r0;
    u32 var_r4;
    u32 var_r5;

    var_r5 = arg0;
    var_r4 = M2C_FIELD(native_utility_child_arm9_data_0202920c, u32 *, 8);
    if (var_r4 == 0) {
        return 0U;
    }
    native_utility_child_arm9_thumb_02010b5c(arg1 + 0x100, 0xA001U);
    sp0 = 0;
    do {
        M2C_FIELD(var_r5, s16 *, 0xFE) = (s16) native_utility_child_arm9_thumb_02010b00(arg1 + 0x100, var_r5, 0xFEU);
loop_4:
        native_utility_child_arm9_thumb_02007ac0(var_r4, 0x100U, var_r5);
        if (native_utility_child_arm9_thumb_02007b08(var_r5, var_r4, 0x100U, arg1) == 0) {
            goto loop_4;
        }
        var_r5 += 0x100;
        temp_r0 = sp0 + 1;
        sp0 = temp_r0;
        var_r4 += 0x100;
    } while (temp_r0 < 4);
    if (native_utility_child_arm9_thumb_02007b38() != 0) {
        return 1U;
    }
    return 0U;
}
