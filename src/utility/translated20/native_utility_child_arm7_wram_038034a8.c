typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037febe8(u32);
#define native_utility_child_arm7_data_040001c0 ((volatile u16 *)0x40001c0)
#define native_utility_child_arm7_data_040001c2 ((volatile u16 *)0x40001c2)
#define native_utility_child_arm7_data_03808168 ((volatile u16 *)0x3808168)
#define native_utility_child_arm7_data_04000136 ((volatile u16 *)0x4000136)
u32 native_utility_child_arm7_wram_038034a8(void) {
    native_utility_child_arm7_thumb_037febe8(0x8000U);
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    *native_utility_child_arm7_data_040001c0 = 0x8A01;
    *native_utility_child_arm7_data_040001c2 = 0x84;
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    *native_utility_child_arm7_data_040001c2 = 0;
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    *native_utility_child_arm7_data_040001c0 = 0x8201;
    *native_utility_child_arm7_data_040001c2 = 0;
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    if (*native_utility_child_arm7_data_03808168 == 0) {
        if (!(*native_utility_child_arm7_data_04000136 & 0x40)) {
            return 1U;
        }
        return 0U;
    }
    if (!(*native_utility_child_arm7_data_04000136 & 0x40)) {
        return 1U;
    }
    *native_utility_child_arm7_data_040001c0 = 0x8A01;
    *native_utility_child_arm7_data_040001c2 = 0x84;
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    *native_utility_child_arm7_data_040001c2 = 0;
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    *native_utility_child_arm7_data_040001c0 = 0x8201;
    *native_utility_child_arm7_data_040001c2 = 0;
    do {

    } while (*native_utility_child_arm7_data_040001c0 & 0x80);
    if (*native_utility_child_arm7_data_04000136 & 0x40) {
        return 0U;
    }
    return 2U;
}
