typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027ec2b8(u32);
u32 native_utility_child_arm7_main_027ec52c(u32 arg0, s16 arg1) {
    void *temp_r0;

    temp_r0 = (void *) native_utility_child_arm7_arm_027ec2b8(arg0);
    M2C_FIELD(temp_r0, s16 *, 0xE) = arg1;
    return (u32) temp_r0;
}
