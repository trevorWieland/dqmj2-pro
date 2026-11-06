typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_04000240[];
extern u8 native_utility_child_arm9_data_04000241[];
extern u8 native_utility_child_arm9_data_04000242[];
extern u8 native_utility_child_arm9_data_04000243[];
extern u8 native_utility_child_arm9_data_04000244[];
extern u8 native_utility_child_arm9_data_04000245[];
extern u8 native_utility_child_arm9_data_04000246[];
extern u8 native_utility_child_arm9_data_04000248[];
extern u8 native_utility_child_arm9_data_04000249[];
void native_utility_child_arm9_main_02008818(s32 arg0) {
    if (arg0 & 1) {
        *native_utility_child_arm9_data_04000240 = 0x80;
    }
    if (arg0 & 2) {
        *native_utility_child_arm9_data_04000241 = 0x80;
    }
    if (arg0 & 4) {
        *native_utility_child_arm9_data_04000242 = 0x80;
    }
    if (arg0 & 8) {
        *native_utility_child_arm9_data_04000243 = 0x80;
    }
    if (arg0 & 0x10) {
        *native_utility_child_arm9_data_04000244 = 0x80;
    }
    if (arg0 & 0x20) {
        *native_utility_child_arm9_data_04000245 = 0x80;
    }
    if (arg0 & 0x40) {
        *native_utility_child_arm9_data_04000246 = 0x80;
    }
    if (arg0 & 0x80) {
        *native_utility_child_arm9_data_04000248 = 0x80;
    }
    if (arg0 & 0x100) {
        *native_utility_child_arm9_data_04000249 = 0x80;
    }
}
