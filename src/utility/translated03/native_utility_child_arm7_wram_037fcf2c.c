typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fd0a4(void);
extern u32 native_utility_child_arm7_arm_037fcf64(void);
extern u32 native_utility_child_arm7_arm_037fc0b8(void);
extern u32 native_utility_child_arm7_arm_037fbdec(void);
extern u32 native_utility_child_arm7_arm_037fd86c(void);
extern u32 native_utility_child_arm7_arm_037fdce0(void);
extern u32 native_utility_child_arm7_arm_037fc6fc(void);
extern u32 native_utility_child_arm7_arm_037fe594(void);
extern u32 native_utility_child_arm7_arm_037fcf70(void);
u32 native_utility_child_arm7_wram_037fcf2c(void) {
    native_utility_child_arm7_arm_037fd0a4();
    native_utility_child_arm7_arm_037fcf64();
    native_utility_child_arm7_arm_037fc0b8();
    native_utility_child_arm7_arm_037fbdec();
    native_utility_child_arm7_arm_037fd86c();
    native_utility_child_arm7_arm_037fdce0();
    native_utility_child_arm7_arm_037fc6fc();
    native_utility_child_arm7_arm_037fe594();
    return native_utility_child_arm7_arm_037fcf70();
}
