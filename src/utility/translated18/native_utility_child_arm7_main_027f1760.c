typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037f8aa4(u32);
extern u32 native_utility_child_arm7_arm_027ec738(u32);
extern u32 native_utility_child_arm7_arm_027efc54(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
void native_utility_child_arm7_main_027f1760(s32 arg0, s32 arg1) {
    u32 var_r8;
    u32 temp_r7;
    s32 temp_r6;
    u32 temp_fp;

    temp_r6 = arg0 * 0xC;
    var_r8 = M2C_FIELD((*native_utility_child_arm7_data_0380fff4 + temp_r6), u32 *, 0x194);
    if (var_r8 != -1U) {
        do {
            temp_fp = native_utility_child_arm7_arm_037f8aa4(var_r8);
            temp_r7 = var_r8 + 0x10;
            if (arg0 != 2) {
                native_utility_child_arm7_arm_027ec738(temp_r7);
            }
            M2C_FIELD(temp_r7, s16 *, 8) = 2;
            if (arg1 != 0) {
                native_utility_child_arm7_arm_027efc54(*native_utility_child_arm7_data_0380fff4 + 0x194 + temp_r6, var_r8);
            }
            var_r8 = temp_fp;
        } while (temp_fp != -1U);
    }
}
