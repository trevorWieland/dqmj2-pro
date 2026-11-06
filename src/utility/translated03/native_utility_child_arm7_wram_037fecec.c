typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_04000501[];
void native_utility_child_arm7_wram_037fecec(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_r6;

    if (*native_utility_child_arm7_data_04000501 & 0x80) {
        var_r6 = 1;
    } else {
        var_r6 = 0;
    }
    *native_utility_child_arm7_data_04000501 = arg0 | ((arg1 * 4) | ((arg2 * 0x10) | ((var_r6 << 7) | (arg3 << 5))));
}
