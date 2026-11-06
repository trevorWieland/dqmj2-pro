typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_0200d0c0(u32 arg0) {
    s32 var_r5;
    u32 var_r4;
    s32 var_r3;
    s32 var_r3_2;
    s32 var_r2;
    s32 var_r1;

    var_r4 = 0;
    var_r5 = 0;
    var_r3 = 0;
loop_1:
    if ((u32) ((arg0 >> var_r3) & 0xF) >= 0xAU) {
        return 0U;
    }
    var_r3 += 4;
    var_r5 += 1;
    if (var_r5 >= 8) {
        var_r1 = 0;
        var_r3_2 = 1;
        var_r2 = 0;
        do {
            var_r4 += ((arg0 >> var_r2) & 0xF) * var_r3_2;
            var_r2 += 4;
            var_r1 += 1;
            var_r3_2 *= 0xA;
        } while (var_r1 < 8);
        return var_r4;
    }
    goto loop_1;
}
