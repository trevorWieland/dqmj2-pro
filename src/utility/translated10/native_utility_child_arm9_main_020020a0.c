typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_020020d8(u32, u32, u32, u32, u32, u32);
extern u8 native_utility_child_arm9_data_02022140[];
extern u8 native_utility_child_arm9_data_02022170[];
u32 native_utility_child_arm9_main_020020a0(void) {
    native_utility_child_arm9_thumb_020020d8((u32) native_utility_child_arm9_data_02022140, 0U, 0xA8U, 0U, 0xE8U, 4U);
    return native_utility_child_arm9_thumb_020020d8((u32) native_utility_child_arm9_data_02022170, 0x84U, 0xACU, 0x84U, 0xECU, 4U);
}
