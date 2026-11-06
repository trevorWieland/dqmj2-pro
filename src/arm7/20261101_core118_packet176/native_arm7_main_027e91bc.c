typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_host_arm7_arm_027ead30(u32, u32);
extern u32 native_host_arm7_runtime_word_0380fff4;
u32 native_arm7_main_027e91bc(u32 arg0, u32 arg1) {
    u32 temp_r0;
    s32 temp_r5;

    if (arg0 < 0xAU) {
        return 5U;
    }
    M2C_FIELD(native_host_arm7_runtime_word_0380fff4, s16 *, 0x33C) = arg0;
    if (arg1 != 0) {
        (*(volatile u16 *)0x04808134) = arg0;
    }
    if (M2C_FIELD(native_host_arm7_runtime_word_0380fff4, u16 *, 0x4A4) != 0) {
        temp_r5 = M2C_FIELD(native_host_arm7_runtime_word_0380fff4, s32 *, 0x4AC) + 0x24 + M2C_FIELD(native_host_arm7_runtime_word_0380fff4, u16 *, 0x3DA);
        temp_r0 = temp_r5 + 6;
        if (M2C_FIELD(native_host_arm7_runtime_word_0380fff4, u16 *, 0x352) == 1) {
            native_host_arm7_arm_027ead30(temp_r0, (u32) (u8) arg0);
            native_host_arm7_arm_027ead30(temp_r5 + 7, (u32) (u8) ((s32) arg0 >> 8));
        } else {
            native_host_arm7_arm_027ead30(temp_r0, 0xFFU);
            native_host_arm7_arm_027ead30(temp_r5 + 7, 0xFFU);
        }
    }
    return 0U;
}
