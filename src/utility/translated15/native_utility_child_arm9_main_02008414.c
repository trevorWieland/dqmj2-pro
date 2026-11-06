typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_02029268[];
extern u32 native_utility_child_arm9_data_04000240[];
extern u8 native_utility_child_arm9_data_04000244[];
extern u8 native_utility_child_arm9_data_04000245[];
extern u8 native_utility_child_arm9_data_04000246[];
extern u16 native_utility_child_arm9_data_04000248[];
u32 native_utility_child_arm9_main_02008414(void) {
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 2) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 4) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 6) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 8) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0xA) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0xC) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0xE) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0x10) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0x12) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0x14) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0x16) = 0;
    M2C_FIELD(native_utility_child_arm9_data_02029268, s16 *, 0x18) = 0;
    *native_utility_child_arm9_data_04000240 = 0;
    *native_utility_child_arm9_data_04000244 = 0;
    *native_utility_child_arm9_data_04000245 = 0;
    *native_utility_child_arm9_data_04000246 = 0;
    *native_utility_child_arm9_data_04000248 = 0;
    return (u32) native_utility_child_arm9_data_04000248;
}
