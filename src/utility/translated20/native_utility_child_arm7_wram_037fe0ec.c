typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbd44(u32, u32);
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
extern u32 native_utility_child_arm7_arm_037fde68(void);
#define native_utility_child_arm7_data_04000004 ((volatile u16 *)0x4000004)
u32 native_utility_child_arm7_wram_037fe0ec(void *arg0) {
    s16 temp_ip;

    native_utility_child_arm7_arm_037fbd44(4U, (u32) native_utility_child_arm7_arm_037fde68);
    temp_ip = M2C_FIELD(arg0, s16 *, 0x10);
    *native_utility_child_arm7_data_04000004 = (*native_utility_child_arm7_data_04000004 & 0x3F) | ((u8) temp_ip << 8) | ((s32) (temp_ip & 0x100) >> 1);
    *native_utility_child_arm7_data_04000004 |= 0x20;
    return native_utility_child_arm7_arm_037fbc8c(4U);
}
