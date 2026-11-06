typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f1cc4(void);
extern u32 native_utility_child_arm7_arm_027f1c64(void);
extern u32 native_utility_child_arm7_arm_027f1bac(void);
u32 native_utility_child_arm7_main_027efc8c(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 2) = 1;
    if (M2C_FIELD(arg0, u16 *, 0x10) & 1) {
        native_utility_child_arm7_arm_027f1cc4();
    }
    if (M2C_FIELD(arg0, u16 *, 0x10) & 2) {
        native_utility_child_arm7_arm_027f1c64();
    }
    if (M2C_FIELD(arg0, u16 *, 0x10) & 4) {
        native_utility_child_arm7_arm_027f1bac();
    }
    return 0U;
}
