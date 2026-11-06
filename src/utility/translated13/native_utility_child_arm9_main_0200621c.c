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
u32 native_utility_child_arm9_main_0200621c(u32 arg0) {
    void *temp_r2;

    temp_r2 = M2C_FIELD(*native_utility_child_arm9_data_02028710, void **, 0x84);
    if (arg0 >= (u32) M2C_FIELD(temp_r2, u32 *, 8)) {
        return 0U;
    }
    return M2C_FIELD((temp_r2 + (arg0 * 0x10)), u32 *, 0x10);
}
