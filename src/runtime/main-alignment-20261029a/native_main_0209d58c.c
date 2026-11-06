typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02096d04();
extern u32 native_fn_02096d24();
extern u32 native_fn_02096d9c();
extern u32 native_fn_02096dd0();
extern u32 native_fn_02096e2c();
extern u32 native_fn_020973a8();
extern u32 native_fn_0209d134();
extern u32 native_fn_0209d4e0();
extern u8 native_data_021d1b74[] __attribute__((aligned(2)));
u32 native_main_0209d58c(s32 arg0, s32 arg1, s32 arg2) {
    u32 sp18;
    u32 sp14;
    u32 sp10;
    s32 spC;
    s32 sp8;
    s32 sp4;
    s32 sp0;
    s32 temp_r1;
    s32 var_r4;
    s32 var_r5;
    s32 var_r7;
    u32 temp_r0;
    u32 var_r6;

    sp0 = arg0;
    sp18 = -1U;
    sp10 = 0;
    sp4 = arg1;
    sp8 = arg2;
    if (arg1 > 0) {
        var_r6 = sp10;
        spC = sp0;
        var_r7 = sp0;
        do {
            temp_r0 = native_fn_0209d134(sp10);
            sp14 = temp_r0;
            if (temp_r0 != 0) {
                if (temp_r0 == sp8) {
                    sp18 = sp10;
                }
                var_r4 = sp10 + 1;
                if (var_r4 < sp4) {
                    var_r5 = sp0 + (var_r4 * 0xC);
                    do {
                        if (sp14 == native_fn_0209d134((u32) var_r4)) {
                            if ((native_fn_02096d9c(spC) == 2) && (native_fn_02096d9c(var_r5) == 3)) {
                                native_fn_020973a8(var_r7, sp14);
                            }
                            if (native_fn_02096d24(var_r5) != 0) {
                                native_fn_02096dd0(var_r7);
                                if (native_fn_02096d04(M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), s32 *, 0x18) + var_r6) != 0) {
                                    native_fn_02096e2c(M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), s32 *, 0x18) + var_r6, 1);
                                }
                            }
                            native_fn_0209d4e0(sp0, (u32) var_r4, sp10);
                            M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), s8 *, 0x1D) = 1;
                        }
                        var_r4 += 1;
                        var_r5 += 0xC;
                    } while (var_r4 < sp4);
                }
            }
            var_r7 += 0xC;
            spC += 0xC;
            var_r6 += 0xC;
            temp_r1 = sp10 + 1;
            sp10 = temp_r1;
        } while (temp_r1 < sp4);
    }
    return sp18;
}
