typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff640(u32, u32);
u32 native_utility_child_arm7_wram_037ffb20(void *arg0, u32 arg1) {
    u8 temp_r2;

    temp_r2 = M2C_FIELD(arg0, u8 *, 0);
    if ((u32) temp_r2 < 0xEU) {
        return 0U;
    }
    if ((u32) temp_r2 > 0xFU) {
        return 0U;
    }
    M2C_FIELD(arg0, s8 *, 1) = 2;
    M2C_FIELD(arg0, s16 *, 0x3C) = 0x1F46;
    native_utility_child_arm7_thumb_037ff640((u32) arg0, arg1);
    return 1U;
}
