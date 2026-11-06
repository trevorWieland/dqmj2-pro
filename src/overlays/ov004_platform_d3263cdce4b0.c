typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
extern u32 func_020081fc(void *);
extern u32 func_02008218(void *);
extern u8 data_ov004_021d8eb4[];

u32 native_ov004_021d8168(void) {
    u8 *var_r1_2;
    s32 var_r1;
    s32 var_r2_2;
    s32 var_r4;
    u8 sp0[90];
    u8 *var_r2;
    u8 *var_r3;

    func_020081fc(sp0);
    var_r3 = data_ov004_021d8eb4;
    var_r2 = sp0;
    var_r4 = 0;
loop_1:
    if (*var_r3 == (*var_r2 ^ 0xFF)) {
        var_r4 += 1;
        var_r2 += 1;
        var_r3 += 1;
        if (var_r4 < 6) {
            goto loop_1;
        }
    }
    func_02008218(sp0 + 6);
    if ((var_r4 == 6) && (sp0[8] == 1) && (sp0[9] == 1) && (*(u16 *)(sp0 + 0x20) == 0)) {
        var_r1 = 0xFB;
    } else {
        var_r1_2 = sp0;
        var_r2_2 = 0;
loop_9:
        if (*var_r1_2 != 0) {
            var_r1 = 0xF1;
        } else {
            var_r2_2 += 1;
            var_r1_2 += 1;
            if (var_r2_2 >= 6) {
                var_r1 = 0xFB;
            } else {
                goto loop_9;
            }
        }
    }
    return var_r1 * 0xC5;
}

u32 native_ov004_021d8218(void) {
    u8 *var_r1_2;
    s32 var_r1;
    s32 var_r2_2;
    s32 var_r4;
    u8 sp0[90];
    u8 *var_r2;
    u8 *var_r3;

    func_020081fc(sp0);
    var_r3 = data_ov004_021d8eb4;
    var_r2 = sp0;
    var_r4 = 0;
loop_1:
    if (*var_r3 == (*var_r2 ^ 0xFF)) {
        var_r4 += 1;
        var_r2 += 1;
        var_r3 += 1;
        if (var_r4 < 6) {
            goto loop_1;
        }
    }
    func_02008218(sp0 + 6);
    if ((var_r4 == 6) && (sp0[8] == 1) && (sp0[9] == 1) && (*(u16 *)(sp0 + 0x20) == 0)) {
        var_r1 = 0xF1;
    } else {
        var_r1_2 = sp0;
        var_r2_2 = 0;
loop_9:
        if (*var_r1_2 != 0) {
            var_r1 = 0xFB;
        } else {
            var_r2_2 += 1;
            var_r1_2 += 1;
            if (var_r2_2 >= 6) {
                var_r1 = 0xF1;
            } else {
                goto loop_9;
            }
        }
    }
    return var_r1 * 0xC1;
}
