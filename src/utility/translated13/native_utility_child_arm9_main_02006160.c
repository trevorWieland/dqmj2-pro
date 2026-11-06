typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_data_02028710[];
u32 native_utility_child_arm9_main_02006160(s32 arg0, s32 arg1) {
    void *temp_r0;

    temp_r0 = M2C_FIELD(*native_utility_child_arm9_data_02028710, s32 *, 0x84) + (arg0 * 0x10);
    M2C_FIELD(temp_r0, s32 *, 0x14) = arg1;
    return (u32) temp_r0;
}
