typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200a7f4(u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
extern u32 native_utility_child_arm9_data_0202961c[];
extern u16 native_utility_child_arm9_data_02029620[];
u32 native_utility_child_arm9_main_0200a7fc(s32 arg0, s32 arg1) {
    s32 temp_r0;
    s32 temp_r2;
    s32 temp_r2_2;
    u32 var_r5;
    u32 sp0;

    sp0 = native_utility_child_arm9_arm_0200a64c();
    var_r5 = arg0 & *native_utility_child_arm9_data_0202961c & 0x1FF;
loop_1:
    temp_r2 = 0x1F - native_utility_child_arm9_arm_0200a7f4(var_r5);
    if (temp_r2 >= 0) {
        temp_r0 = 1 << temp_r2;
        var_r5 &= ~temp_r0;
        temp_r2_2 = temp_r2;
        if (arg1 == *(native_utility_child_arm9_data_02029620 + temp_r2_2)) {
            *(native_utility_child_arm9_data_02029620 + temp_r2_2) = 0;
            *native_utility_child_arm9_data_0202961c &= ~temp_r0;
        }
        goto loop_1;
    }
    return native_utility_child_arm9_arm_0200a660(sp0);
}
