typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02027cd8[];
u32 native_utility_child_arm9_main_020024cc(void) {
    M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), s32 *, 0xA44) = 0xE;
    return 0xA44U;
}
