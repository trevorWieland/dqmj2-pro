typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_027e2104[];
u32 native_utility_child_arm7_main_027e21dc(s32 arg0) {
    return ((u32 (*)(s32, s32, s32)) native_utility_child_arm7_data_027e2104)(arg0, 0x307, 0x5C);
}
