typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_040001c0 ((volatile u16 *)0x40001c0)
#define native_utility_child_arm7_data_040001c2 ((volatile u16 *)0x40001c2)
u32 native_utility_child_arm7_main_027f61e0(void) {
    u32 temp_r0;

    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    *native_utility_child_arm7_data_040001c0 = 0x8100;
    *native_utility_child_arm7_data_040001c2 = 0xC7;
    do {
        temp_r0 = *native_utility_child_arm7_data_040001c0 & 0x80;
    } while (temp_r0 != 0);
    return temp_r0;
}
