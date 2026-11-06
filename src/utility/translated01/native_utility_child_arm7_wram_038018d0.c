typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_038018e1(u32, u32);
extern u32 native_utility_child_arm7_thumb_037feae1(u32, u32);
u32 native_utility_child_arm7_wram_038018d0(void) {
    return native_utility_child_arm7_thumb_037feae1(7U, (u32) native_utility_child_arm7_thumb_038018e1);
}
