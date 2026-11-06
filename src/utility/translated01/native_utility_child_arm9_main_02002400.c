typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_020023b4(u32, u32, u32, u32);
u32 native_utility_child_arm9_main_02002400(void) {
    return native_utility_child_arm9_thumb_020023b4(0x85U, 0xAAU, 0xF9U, 0xC0U);
}
