typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f8d4(void);
extern u32 native_utility_child_arm9_thumb_0200fa74(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200f86d(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_data_0202cbc4[];
u32 native_utility_child_arm9_main_0200f8b0(void) {
    native_utility_child_arm9_thumb_0200f8d4();
    native_utility_child_arm9_thumb_0200fa74(0xEU, (u32) native_utility_child_arm9_thumb_0200f86d);
    *native_utility_child_arm9_data_0202cbc4 = 0;
    return (u32) native_utility_child_arm9_data_0202cbc4;
}
