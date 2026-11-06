typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_host_arm7_arm_027e91bc(u32, u32);
extern u32 native_host_arm7_runtime_word_0380fff4;

u32 native_arm7_main_027e9c58(u32 arg0) {
    void *temp_r3;

    temp_r3 = native_host_arm7_runtime_word_0380fff4 + 0x31C;
    M2C_FIELD(native_host_arm7_runtime_word_0380fff4, s16 *, 0x352) = arg0;
    if ((arg0 != 0) && (M2C_FIELD(temp_r3, u16 *, 0x12) != 1)) {
        (*(volatile u16 *)0x04808006) |= 0x40;
    } else {
        (*(volatile u16 *)0x04808006) &= ~0x40;
        native_host_arm7_arm_027e91bc((u32) M2C_FIELD(temp_r3, u16 *, 0x20), 0U);
    }
    return 0U;
}
