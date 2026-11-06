typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_04000501 ((volatile u8 *)0x4000501)
u32 native_utility_child_arm7_wram_037fedc8(void) {
    *native_utility_child_arm7_data_04000501 &= ~0x80;
    return 0x80U;
}
