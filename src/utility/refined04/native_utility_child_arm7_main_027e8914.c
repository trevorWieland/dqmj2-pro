typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e2354(u32, u32);
extern u32 native_utility_child_arm7_arm_027e88d8(u32, u32);
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
u32 native_utility_child_arm7_main_027e8914(void *arg0) {
    u8 sp0[516];
    u16 temp_r1;
    void *temp_r0;

    temp_r1 = M2C_FIELD((void *) native_utility_child_arm7_arm_027e2354((u32) &sp0, (u32) (u16) M2C_FIELD(arg0, s32 *, 4)), u16 *, 4);
    if (temp_r1 != 0) {
        return native_utility_child_arm7_arm_027e88d8(0x242U, (u32) temp_r1);
    }
    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 0) = 0x24;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
