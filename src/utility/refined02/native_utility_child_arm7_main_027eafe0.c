typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027eafe0(u32 arg0) {
    if (arg0 > 1U) {
        return 5U;
    }
    M2C_FIELD(*native_utility_child_arm7_data_0380fff4, s16 *, 0x332) = (s16) arg0;
    return 0U;
}
