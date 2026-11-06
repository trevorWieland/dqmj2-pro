typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027ec14c(u32);
extern u32 native_utility_child_arm7_arm_027ec2f0(u32);
extern u32 native_utility_child_arm7_arm_027ec2b8(u32);
extern u32 native_utility_child_arm7_arm_027ea414(void);
extern u32 native_utility_child_arm7_data_0380fff4[];
void native_utility_child_arm7_main_027ec3e4(u32 arg0) {
    u32 temp_r0;
    u32 temp_r5;

    temp_r5 = *native_utility_child_arm7_data_0380fff4;
    native_utility_child_arm7_arm_027ec14c(arg0);
    temp_r0 = native_utility_child_arm7_arm_027ec2f0(arg0);
    if (temp_r0 != 0) {
        M2C_FIELD((void *) native_utility_child_arm7_arm_027ec2b8(arg0), s16 *, 2) = 0;
        M2C_FIELD(temp_r5, u16 *, 0x53A) = (u16) (M2C_FIELD(temp_r5, u16 *, 0x53A) & ~(1 << temp_r0));
        M2C_FIELD(temp_r5, u16 *, 0x538) = (u16) (M2C_FIELD(temp_r5, u16 *, 0x538) - 1);
        if (M2C_FIELD(temp_r5, u16 *, 0x538) == 0) {
            native_utility_child_arm7_arm_027ea414();
        }
    }
}
