typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02009eac(u32, u32);
u32 native_utility_child_arm9_main_0200b698(void *arg0) {
    s32 var_r6;
    s32 var_r5;
    void *var_r4;
    void *var_r4_2;
    s32 var_r3_2;
    void *var_r3;

    var_r6 = 0;
    M2C_FIELD(arg0, s32 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xA) = 0;
    M2C_FIELD(arg0, s32 *, 0) = 0;
    var_r4 = arg0;
    do {
        M2C_FIELD(var_r4, s32 *, 0x40) = 0;
        var_r5 = 0;
        var_r3 = var_r4;
loop_2:
        M2C_FIELD(var_r3, s16 *, 0x20) = -1;
        var_r3 += 2;
        var_r5 += 1;
        if (var_r5 < 0x10) {
            goto loop_2;
        }
        var_r4 += 0x24;
        var_r6 += 1;
    } while (var_r6 < 0x10);
    var_r3_2 = 0;
    var_r4_2 = arg0;
    do {
        M2C_FIELD(var_r4_2, s16 *, 0x260) = -1;
        var_r4_2 += 2;
        var_r3_2 += 1;
    } while (var_r3_2 < 0x10);
    return native_utility_child_arm9_arm_02009eac((u32) arg0, 0x280U);
}
