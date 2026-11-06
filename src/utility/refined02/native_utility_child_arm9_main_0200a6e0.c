typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200a888(void);
extern u16 native_utility_child_arm9_data_02029618[];
u32 native_utility_child_arm9_main_0200a6e0(u32 arg0, s32 arg1) {
    if (((u32) ((arg1 & 0x7F00) << 8) >> 0x10) == 0x10) {
        *native_utility_child_arm9_data_02029618 = 1;
        return (u32) native_utility_child_arm9_data_02029618;
    }
    return native_utility_child_arm9_thumb_0200a888();
}
