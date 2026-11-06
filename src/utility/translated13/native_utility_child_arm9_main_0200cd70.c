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
extern u16 native_utility_child_arm9_data_0202b210[];
u32 native_utility_child_arm9_main_0200cd70(u32 arg0, s32 arg1) {
    if ((arg1 & 0x3F) == 1) {
        *native_utility_child_arm9_data_0202b210 = 1;
        return (u32) native_utility_child_arm9_data_0202b210;
    }
    return native_utility_child_arm9_thumb_0200a888();
}
