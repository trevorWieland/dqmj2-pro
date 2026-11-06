typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fa4b4(void);
extern u32 native_utility_child_arm7_arm_037fa5ec(void);
extern u32 native_utility_child_arm7_arm_037f9538(void);
extern u32 native_utility_child_arm7_arm_037f95c4(void);
extern u32 native_utility_child_arm7_arm_037f98c0(void);
extern u32 native_utility_child_arm7_arm_027ebd00(void);
extern u32 native_utility_child_arm7_arm_037f9978(void);
extern u32 native_utility_child_arm7_arm_037f9aa4(void);
extern u32 native_utility_child_arm7_arm_037f9f14(void);
extern u32 native_utility_child_arm7_arm_037f993c(void);
extern u32 native_utility_child_arm7_arm_037f9c68(void);
extern u32 native_utility_child_arm7_arm_037fa3a4(u32);
#define native_utility_child_arm7_data_04808010 ((volatile u16 *)0x4808010)
#define native_utility_child_arm7_data_04808012 ((volatile u16 *)0x4808012)
#define native_utility_child_arm7_data_0380fff8 ((volatile u32 *)0x380fff8)
u32 native_utility_child_arm7_wram_037f9454(void) {
    u32 temp_r0;
    s32 temp_r6;

loop_1:
    temp_r6 = *native_utility_child_arm7_data_04808010 & *native_utility_child_arm7_data_04808012;
    if (temp_r6 != 0) {
        if (temp_r6 & 0x80) {
            native_utility_child_arm7_arm_037fa4b4();
        }
        if (temp_r6 & 0x40) {
            native_utility_child_arm7_arm_037fa5ec();
        }
        if (temp_r6 & 0x8000) {
            native_utility_child_arm7_arm_037f9538();
        }
        if (temp_r6 & 0x4000) {
            native_utility_child_arm7_arm_037f95c4();
        }
        if (temp_r6 & 0x2000) {
            native_utility_child_arm7_arm_037f98c0();
        }
        if (temp_r6 & 0x800) {
            native_utility_child_arm7_arm_027ebd00();
        }
        if (temp_r6 & 8) {
            native_utility_child_arm7_arm_037f9978();
        }
        if (temp_r6 & 4) {
            native_utility_child_arm7_arm_037f9aa4();
        }
        if (temp_r6 & 1) {
            native_utility_child_arm7_arm_037f9f14();
        }
        if (temp_r6 & 0x30) {
            native_utility_child_arm7_arm_037f993c();
        }
        if (temp_r6 & 2) {
            native_utility_child_arm7_arm_037f9c68();
        }
        if (temp_r6 & 0x1000) {
            native_utility_child_arm7_arm_037fa3a4(1U);
        }
        goto loop_1;
    }
    temp_r0 = *native_utility_child_arm7_data_0380fff8 | 0x01000000;
    *native_utility_child_arm7_data_0380fff8 = temp_r0;
    return temp_r0;
}
