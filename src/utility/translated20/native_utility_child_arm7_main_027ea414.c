typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_0380fff4 ((volatile u32 *)0x380fff4)
#define native_utility_child_arm7_data_04808038 ((volatile u16 *)0x4808038)
#define native_utility_child_arm7_data_04808048 ((volatile u16 *)0x4808048)
u32 native_utility_child_arm7_main_027ea414(void) {
    u16 temp_r0;

    M2C_FIELD(*native_utility_child_arm7_data_0380fff4, s16 *, 0x3EA) = 1;
    temp_r0 = M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x468);
    if (temp_r0 != 0) {
        return (u32) temp_r0;
    }
    *native_utility_child_arm7_data_04808038 &= ~2;
    *native_utility_child_arm7_data_04808048 = 0;
    return (u32) native_utility_child_arm7_data_04808048;
}
