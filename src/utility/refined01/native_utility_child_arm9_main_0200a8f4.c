typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200a888(void);
extern u32 native_utility_child_arm9_data_040000b8[];
void native_utility_child_arm9_main_0200a8f4(s32 arg0, s32 arg1) {
    s32 sp0;
    s32 temp_r0;
    s32 temp_r0_2;
    s32 var_r4;
    u32 *var_r6;

    sp0 = arg0;
    var_r4 = 0;
    var_r6 = native_utility_child_arm9_data_040000b8;
    do {
        if (var_r4 != sp0) {
            temp_r0 = *var_r6;
            if (temp_r0 & 0x80000000) {
                temp_r0_2 = temp_r0 & 0x38000000;
                if ((temp_r0_2 != arg1) && ((temp_r0_2 != 0x08000000) || (arg1 != 0x10000000)) && ((temp_r0_2 != 0x10000000) || (arg1 != 0x08000000)) && ((temp_r0_2 == 0x18000000) || (temp_r0_2 == 0x20000000) || (temp_r0_2 == 0x28000000) || (temp_r0_2 == 0x30000000) || (temp_r0_2 == 0x38000000) || (temp_r0_2 == 0x08000000) || (temp_r0_2 == 0x10000000))) {
                    native_utility_child_arm9_thumb_0200a888();
                }
            }
        }
        var_r6 += 3;
        var_r4 += 1;
    } while (var_r4 < 3);
}
