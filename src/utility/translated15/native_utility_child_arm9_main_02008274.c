typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u16 native_utility_child_arm9_data_020225c0[];
extern u16 native_utility_child_arm9_data_02029264[];
extern u32 native_utility_child_arm9_data_04000000[];
void native_utility_child_arm9_main_02008274(void) {
    *native_utility_child_arm9_data_020225c0 = 1;
    if (*native_utility_child_arm9_data_02029264 != 0) {
        *native_utility_child_arm9_data_04000000 = (*native_utility_child_arm9_data_04000000 & 0xFFFCFFFF) | (*native_utility_child_arm9_data_02029264 << 0x10);
        return;
    }
    *native_utility_child_arm9_data_04000000 |= 0x10000;
}
