typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_038027b4(void);
extern u32 native_utility_child_arm7_thumb_03802790(void);
extern u32 native_utility_child_arm7_data_03807be8[];
extern u8 native_utility_child_arm7_data_027ffc1f[];
u32 native_utility_child_arm7_wram_03802800(void) {
    if (*native_utility_child_arm7_data_03807be8 == 0) {
        if (*native_utility_child_arm7_data_027ffc1f & 1) {
            native_utility_child_arm7_thumb_038027b4();
        } else {
            native_utility_child_arm7_thumb_03802790();
        }
    }
    return *native_utility_child_arm7_data_03807be8;
}
