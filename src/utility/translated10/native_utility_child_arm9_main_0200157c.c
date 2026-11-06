typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200172c(void);
extern u32 native_utility_child_arm9_arm_02004dd4(u32, u32, u32, u32, u32, u32, u32, u32);
extern u8 native_utility_child_arm9_data_02026610[];
extern u8 native_utility_child_arm9_data_02026660[];
extern u8 native_utility_child_arm9_data_02026620[];
u32 native_utility_child_arm9_main_0200157c(void) {
    M2C_FIELD(native_utility_child_arm9_data_02026610, s32 (**)(u8 *, s32), 0x68)(native_utility_child_arm9_data_02026660, 0);
    return native_utility_child_arm9_arm_02004dd4((u32) native_utility_child_arm9_data_02026620, 6U, 0U, 0xE4U, 0x70U, 2U, 0x80 | M2C_FIELD(native_utility_child_arm9_data_02026610, s32 *, 0), native_utility_child_arm9_thumb_0200172c());
}
