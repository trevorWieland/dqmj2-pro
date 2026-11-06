typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
u32 native_utility_child_arm7_main_027e4a90(s16 arg0, s16 arg1, s16 arg2, s16 arg3) {
    void *temp_r0;

    temp_r0 = (void *) native_utility_child_arm7_arm_0380576c();
    M2C_FIELD(temp_r0, s16 *, 0) = 0x25;
    M2C_FIELD(temp_r0, s16 *, 2) = 1;
    M2C_FIELD(temp_r0, s16 *, 4) = arg0;
    M2C_FIELD(temp_r0, s16 *, 6) = arg1;
    M2C_FIELD(temp_r0, s16 *, 8) = arg2;
    M2C_FIELD(temp_r0, s16 *, 0xA) = arg3;
    return native_utility_child_arm7_arm_038057c8((u32) temp_r0);
}
