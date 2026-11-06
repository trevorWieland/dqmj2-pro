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
extern u32 native_utility_child_arm7_arm_037fbc50(u32);
extern u32 native_utility_child_arm7_arm_027ec14c(u32);
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027ec738(void *arg0) {
    u32 temp_r6;
    u32 temp_r5;
    u16 temp_r4;

    temp_r4 = M2C_FIELD(arg0, u16 *, 2);
    temp_r6 = native_utility_child_arm7_arm_027ec2b8((u32) temp_r4);
    temp_r5 = native_utility_child_arm7_arm_037fbc50(0x01000000U);
    if ((M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x350) == 1) && (M2C_FIELD(temp_r6, u16 *, 0x16) == 1)) {
        native_utility_child_arm7_arm_027ec14c((u32) temp_r4);
    }
    M2C_FIELD(temp_r6, u16 *, 0x16) = (u16) (M2C_FIELD(temp_r6, u16 *, 0x16) - 1);
    return native_utility_child_arm7_arm_037fbc8c(temp_r5);
}
