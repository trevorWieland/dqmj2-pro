typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f630(u32, u32);
extern u32 native_utility_child_arm9_data_02022614[];
#define native_utility_child_arm9_data_040001a4 ((volatile u32 *)0x40001a4)
#define native_utility_child_arm9_data_04100010 ((volatile u32 *)0x4100010)
u32 native_utility_child_arm9_main_0200f300(void) {
    native_utility_child_arm9_thumb_0200f630(0xB8000000U, 0U);
    *native_utility_child_arm9_data_040001a4 = ((M2C_FIELD(*native_utility_child_arm9_data_02022614, s32 *, 0x60) & 0xF8FFFFFF) | 0xA7000000) & 0xFFFFE000;
    do {

    } while (!(*native_utility_child_arm9_data_040001a4 & 0x800000));
    return *native_utility_child_arm9_data_04100010;
}
