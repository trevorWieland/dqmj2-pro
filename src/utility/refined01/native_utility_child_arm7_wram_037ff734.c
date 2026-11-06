typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff1a4(u32);
u32 native_utility_child_arm7_wram_037ff734(void *arg0) {
    u32 var_r2;

    if (M2C_FIELD(arg0, u8 *, 2) == 0) {
        return 0U;
    }
    if ((u32) M2C_FIELD(arg0, u16 *, 6) < (u32) M2C_FIELD(arg0, u16 *, 4)) {
        var_r2 = 0;
    } else {
        var_r2 = native_utility_child_arm7_thumb_037ff1a4((u32) (u16) M2C_FIELD(arg0, u16 *, 8) >> 8) * M2C_FIELD(arg0, u8 *, 2) * M2C_FIELD(arg0, u8 *, 3);
    }
    return var_r2;
}
