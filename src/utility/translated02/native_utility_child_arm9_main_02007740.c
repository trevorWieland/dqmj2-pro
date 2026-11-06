typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02007740(u8 *arg0) {
    u8 temp_r0;

    temp_r0 = *arg0;
    if (temp_r0 == 0x7F) {
        return 0U;
    }
    if ((u32) temp_r0 < 1U) {
        return 0U;
    }
    if ((u32) temp_r0 <= 0xDFU) {
        return 1U;
    }
    return 0U;
}
