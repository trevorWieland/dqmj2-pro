typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm7_wram_037fde18(void *arg0, s32 arg1, s32 arg2) {
    s32 temp_r3;
    s32 var_r2;

    temp_r3 = arg1 - M2C_FIELD(arg0, s32 *, 0xC);
    var_r2 = arg2 - M2C_FIELD(arg0, s16 *, 0x10);
    if ((temp_r3 < 0) || ((temp_r3 == 0) && (var_r2 < 0))) {
        return 0U;
    }
    if (var_r2 < 0) {
        var_r2 += 0x107;
    }
    if (var_r2 <= (s32) M2C_FIELD(arg0, s16 *, 0x12)) {
        return 1U;
    }
    return 2U;
}
