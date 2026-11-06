typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02008818(u32);
extern u8 native_utility_child_arm9_data_02029268[];
extern u8 native_utility_child_arm9_data_04000242[];
extern u8 native_utility_child_arm9_data_04000249[];
extern u8 native_utility_child_arm9_data_04000248[];
u32 native_utility_child_arm9_main_02008548(u16 arg0) {
    M2C_FIELD(native_utility_child_arm9_data_02029268, u16 *, 0) = (u16) (~arg0 & (M2C_FIELD(native_utility_child_arm9_data_02029268, u16 *, 0) | M2C_FIELD(native_utility_child_arm9_data_02029268, u16 *, 0x12)));
    M2C_FIELD(native_utility_child_arm9_data_02029268, u16 *, 0x12) = arg0;
    switch ((s32) arg0) {
    case 0x0:
        break;
    case 0x4:
        *native_utility_child_arm9_data_04000242 = 0x84;
        break;
    case 0x180:
        *native_utility_child_arm9_data_04000249 = 0x81;
        
    case 0x80:
        *native_utility_child_arm9_data_04000248 = 0x81;
        break;
    }
    return native_utility_child_arm9_thumb_02008818((u32) M2C_FIELD(native_utility_child_arm9_data_02029268, u16 *, 0));
}
