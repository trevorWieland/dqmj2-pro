typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fc180(void);
extern u32 native_utility_child_arm7_arm_037fc2b0(u32, u32);
extern u32 native_utility_child_arm7_arm_027e8b64(void);
extern u32 native_utility_child_arm7_arm_037fc148(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
extern u8 native_utility_child_arm7_data_038091c8[];
extern u8 native_utility_child_arm7_data_027f94f0[];
extern u8 native_utility_child_arm7_data_0380926c[];
u32 native_utility_child_arm7_main_027e0238(void) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm7_arm_037fe41c();
    native_utility_child_arm7_arm_037fc180();
    native_utility_child_arm7_arm_037fc2b0((u32) native_utility_child_arm7_data_038091c8, M2C_FIELD(native_utility_child_arm7_data_027f94f0, u32 *, 0x58C));
    native_utility_child_arm7_arm_037fc2b0(native_utility_child_arm7_arm_027e8b64(), M2C_FIELD(native_utility_child_arm7_data_027f94f0, u32 *, 0x588));
    native_utility_child_arm7_arm_037fc2b0((u32) native_utility_child_arm7_data_0380926c, M2C_FIELD(native_utility_child_arm7_data_027f94f0, u32 *, 0x584));
    native_utility_child_arm7_arm_037fc148();
    return native_utility_child_arm7_arm_037fe430(temp_r4);
}
