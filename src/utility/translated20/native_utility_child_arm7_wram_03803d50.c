typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03803c14(u32);
extern u32 native_utility_child_arm7_thumb_03803968(u32);
#define native_utility_child_arm7_data_04000304 ((volatile u16 *)0x4000304)
u32 native_utility_child_arm7_wram_03803d50(void) {
    *native_utility_child_arm7_data_04000304 &= ~2;
    native_utility_child_arm7_thumb_03803c14(1U);
    return native_utility_child_arm7_thumb_03803968(1U);
}
