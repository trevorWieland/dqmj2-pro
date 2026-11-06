typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02008414(void);
extern u32 native_utility_child_arm9_arm_020091a8(void);
extern u32 native_utility_child_arm9_thumb_0200a888(void);
extern u32 native_utility_child_arm9_thumb_0200aaa8(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_arm_0200ab48(u32, u32, u32);
#define native_utility_child_arm9_data_04000304 ((volatile u16 *)0x4000304)
#define native_utility_child_arm9_data_02029260 ((volatile u16 *)0x2029260)
#define native_utility_child_arm9_data_04000004 ((volatile u16 *)0x4000004)
#define native_utility_child_arm9_data_04000000 ((volatile u32 *)0x4000000)
extern u32 native_utility_child_arm9_data_020225c4[];
#define native_utility_child_arm9_data_04000008 ((volatile u8 *)0x4000008)
#define native_utility_child_arm9_data_0400006c ((volatile u16 *)0x400006c)
#define native_utility_child_arm9_data_04001000 ((volatile u8 *)0x4001000)
#define native_utility_child_arm9_data_04000020 ((volatile u16 *)0x4000020)
#define native_utility_child_arm9_data_04000026 ((volatile u16 *)0x4000026)
#define native_utility_child_arm9_data_04000030 ((volatile u16 *)0x4000030)
#define native_utility_child_arm9_data_04000036 ((volatile u16 *)0x4000036)
#define native_utility_child_arm9_data_04001020 ((volatile u16 *)0x4001020)
#define native_utility_child_arm9_data_04001026 ((volatile u16 *)0x4001026)
#define native_utility_child_arm9_data_04001030 ((volatile u16 *)0x4001030)
#define native_utility_child_arm9_data_04001036 ((volatile u16 *)0x4001036)
u32 native_utility_child_arm9_main_0200830c(void) {
    u32 temp_r0;

    *native_utility_child_arm9_data_04000304 |= 0x8000;
    *native_utility_child_arm9_data_04000304 = (*native_utility_child_arm9_data_04000304 & 0xFFFFFDF1) | 0x20E;
    *native_utility_child_arm9_data_04000304 |= 1;
    native_utility_child_arm9_thumb_02008414();
    if (*native_utility_child_arm9_data_02029260 == 0) {
        do {
            temp_r0 = native_utility_child_arm9_arm_020091a8();
            if (temp_r0 == -3U) {
                native_utility_child_arm9_thumb_0200a888();
            }
            *native_utility_child_arm9_data_02029260 = (u16) temp_r0;
        } while (*native_utility_child_arm9_data_02029260 == 0);
    }
    *native_utility_child_arm9_data_04000004 = 0;
    *native_utility_child_arm9_data_04000000 = 0;
    if (*native_utility_child_arm9_data_020225c4 != -1U) {
        native_utility_child_arm9_thumb_0200aaa8(*native_utility_child_arm9_data_020225c4, (u32) native_utility_child_arm9_data_04000008, 0U, 0x60U);
        *native_utility_child_arm9_data_0400006c = 0;
        native_utility_child_arm9_thumb_0200aaa8(*native_utility_child_arm9_data_020225c4, (u32) native_utility_child_arm9_data_04001000, 0U, 0x70U);
    } else {
        native_utility_child_arm9_arm_0200ab48(0U, (u32) native_utility_child_arm9_data_04000008, 0x60U);
        *native_utility_child_arm9_data_0400006c = 0;
        native_utility_child_arm9_arm_0200ab48(0U, (u32) native_utility_child_arm9_data_04001000, 0x70U);
    }
    *native_utility_child_arm9_data_04000020 = 0x100;
    *native_utility_child_arm9_data_04000026 = 0x100;
    *native_utility_child_arm9_data_04000030 = 0x100;
    *native_utility_child_arm9_data_04000036 = 0x100;
    *native_utility_child_arm9_data_04001020 = 0x100;
    *native_utility_child_arm9_data_04001026 = 0x100;
    *native_utility_child_arm9_data_04001030 = 0x100;
    *native_utility_child_arm9_data_04001036 = 0x100;
    return 0x100U;
}
