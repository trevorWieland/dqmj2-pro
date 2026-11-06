typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_host_arm7_arm_027ea62c(u32);
extern u32 native_host_arm7_arm_037fb420(void);
extern u32 native_host_arm7_arm_027ea5fc(u32, u32);
extern u32 native_host_arm7_runtime_word_0380fff4;




u32 native_arm7_main_027e9d00(void) {
    if (M2C_FIELD(native_host_arm7_runtime_word_0380fff4, u16 *, 0x5F8) == 2) {
        native_host_arm7_arm_027ea62c(0xC008U);
    }
    (*(volatile u16 *)0x04808158) = 0x601E;
    native_host_arm7_arm_037fb420();
    native_host_arm7_arm_027ea5fc(0x1EU, (*(volatile u16 *)0x0480815c) | 0x3F);
    (*(volatile u16 *)0x04808168) = 0x800D;
    (*(volatile u16 *)0x04808036) = 1;
    return 0x04808036U;
}
