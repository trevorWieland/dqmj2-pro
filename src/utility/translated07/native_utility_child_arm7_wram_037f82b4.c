typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037f8334(u32);
extern u32 native_utility_child_arm7_thumb_037f8340(u32);
extern u32 native_utility_child_arm7_thumb_037f834c(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_037f8358(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_037f8364(u32, u32);
extern u32 native_utility_child_arm7_thumb_037f8370(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_037f837c(void);
extern u32 native_utility_child_arm7_thumb_037f8388(u32, u32);
extern u32 native_utility_child_arm7_thumb_037f8394(u32, u32);
u32 native_utility_child_arm7_wram_037f82b4(void) {
    s32 temp_r0;
    u32 temp_r4;
    u32 temp_r4_2;
    u32 temp_r4_3;

    temp_r4 = native_utility_child_arm7_thumb_037f8334(8U);
    temp_r4_2 = native_utility_child_arm7_thumb_037f834c(8U, native_utility_child_arm7_thumb_037f8340(8U), temp_r4, 1U);
    native_utility_child_arm7_thumb_037f8358(temp_r4_2, 0U, native_utility_child_arm7_thumb_037f8334(8U) - temp_r4_2);
    native_utility_child_arm7_thumb_037f8364(8U, temp_r4_2);
    temp_r4_3 = native_utility_child_arm7_thumb_037f8334(8U);
    temp_r0 = (s32) native_utility_child_arm7_thumb_037f8370(8U, native_utility_child_arm7_thumb_037f8340(8U), temp_r4_3);
    if (temp_r0 < 0) {
        native_utility_child_arm7_thumb_037f837c();
    }
    native_utility_child_arm7_thumb_037f8388(8U, (u32) temp_r0);
    if (native_utility_child_arm7_thumb_037f8394(8U, (u32) temp_r0) < 0x2100U) {
        native_utility_child_arm7_thumb_037f837c();
    }
    return (u32) temp_r0;
}
