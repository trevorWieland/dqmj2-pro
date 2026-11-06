typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037f8178(u32, u32, u32);
u32 native_utility_child_arm7_wram_037f8148(void) {
    u8 temp_r1;
    u8 sp0;

    native_utility_child_arm7_thumb_037f8178(0x1DU, 1U, (u32) &sp0);
    temp_r1 = sp0;
    if (temp_r1 == 0xFF) {
        return 0U;
    }
    if (temp_r1 & 0x40) {
        return 1U;
    }
    return 0U;
}
